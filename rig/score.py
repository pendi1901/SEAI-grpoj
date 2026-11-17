#!/usr/bin/env python3
"""
score.py: grade every generated program with one number, Q.

Follows the ten-skill table in the course's gloss10 page: pick a dumb
rival, scale against it so the baseline means "no better than dumb", and
score every failure at the baseline. Higher Q is better.

  python rig/score.py                 # score every call not yet scored
  python rig/score.py --workers 8
  python rig/score.py --config timing/x.json

Each program is graded in its own child process with a time limit, so a
crash or a hang costs that program its baseline and nothing else. Every
program of one skill in one domain faces the same test cases.

Written with LLM help; experiment tooling, not part of treatment 7.
Where this departs from gloss10 is listed in rig/README.md.
"""
import argparse, contextlib, csv, importlib.util, io, json, os, random
import statistics as st, subprocess, sys, threading, time, zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
import run
from contract import BASELINE

FIELDS = ("domain treatment trial step skill q status detail secs dir").split()
LOCK = threading.Lock()

# Repetitions. gloss10's figures are in the comments.
SPLITS, ORDERS, PAIRS = 30, 100, 200     # guess 30; flow 100; certify 200
RUNS, BUDGET = 30, 50                    # choose and race: 30 runs, 50 labels
COPIES, INJECT, TOP = 10, 10, 20         # spot: gloss10 uses 30 copies
POOL = 300                               # rows per choose/race run
CAP = 2000                               # rows sampled from a big table


class Invalid(Exception):
  "The skill answered, but outside the rules."


class Data:
  "A table, with the distance-to-best score the gloss calls disty."
  def __init__(i, path, levers=()):
    rows = list(csv.reader(open(path, encoding="utf8")))
    i.header = [c.strip() for c in rows[0]]
    i.num = [c[0].isupper() for c in i.header]
    i.goal = [k for k, c in enumerate(i.header) if c[-1] in "+-"]
    i.x = [k for k, c in enumerate(i.header) if c[-1] not in "+-"]
    i.rows = [[i.cell(k, v) for k, v in enumerate(r)] for r in rows[1:] if r]
    if len(i.rows) > CAP:
      i.rows = random.Random(1).sample(i.rows, CAP)
    i.lo, i.hi, i.mu, i.sd = {}, {}, {}, {}
    for k, isnum in enumerate(i.num):
      if isnum:
        v = [r[k] for r in i.rows if r[k] != "?"]
        i.lo[k], i.hi[k] = min(v), max(v)
        i.mu[k], i.sd[k] = st.mean(v), st.pstdev(v)
    i.levers = {}
    for name in levers:
      k = i.header.index(name)
      i.levers[name] = ((i.lo[k], i.hi[k]) if i.num[k] else
                        sorted({r[k] for r in i.rows}))

  def cell(i, k, v):
    v = v.strip()
    if v == "?" or not i.num[k]: return v
    try: return float(v)
    except ValueError: return "?"

  def norm(i, k, v):
    return (v - i.lo[k]) / (i.hi[k] - i.lo[k] + 1e-32)

  def d(i, row):
    "0 = every goal at its best; 1 = every goal at its worst."
    s = sum((i.norm(k, row[k]) - (i.header[k][-1] == "+")) ** 2
            for k in i.goal)
    return (s / len(i.goal)) ** .5

  def hide(i, row):
    return [("?" if k in i.goal else v) for k, v in enumerate(row)]

  def gap(i, a, b):
    "Distance between two rows over the input columns only."
    s = 0
    for k in i.x:
      if a[k] == "?" or b[k] == "?": s += 1
      elif i.num[k]: s += (i.norm(k, a[k]) - i.norm(k, b[k])) ** 2
      else: s += a[k] != b[k]
    return s

  def oracle(i, ref):
    "Guess a row's score from its 5 nearest rows in REF, by inputs alone."
    ds = [i.d(r) for r in ref]
    def guess(row):
      near = sorted(range(len(ref)), key=lambda j: i.gap(row, ref[j]))[:5]
      return st.mean(ds[j] for j in near)
    return guess


def indices(got, n):
  "A list of distinct valid row positions, in the order given."
  out = []
  for v in got or []:
    if isinstance(v, bool) or not isinstance(v, int): raise Invalid("not ints")
    if not 0 <= v < n: raise Invalid("position out of range")
    if v not in out: out.append(v)
  return out


def copy(rows): return [r[:] for r in rows]
def clip(q): return max(-1.0, min(1.0, q))


def labeller(D, pool):
  "A label() that counts, and refuses the 51st distinct row."
  asked = set()
  def label(j):
    if j not in asked and len(asked) >= BUDGET:
      raise Invalid("asked for more than 50 labels")
    asked.add(j)
    return [pool[j][k] for k in D.goal]
  return label


def versus_random(D, pool, mine, rnd):
  "Win 1, tie 0.5, loss 0 against the best of 50 random rows."
  rival = min(D.d(r) for r in rnd.sample(pool, min(BUDGET, len(pool))))
  me = D.d(pool[mine])
  return 1 if me < rival - 1e-12 else .5 if me <= rival + 1e-12 else 0


# -- one function per skill: (skill's function, data, rng) -> Q ---------
def q_remember(f, D, rnd):
  got = indices(f(D.header[:], copy(D.rows)), len(D.rows))
  if not got or len(got) > max(1, len(D.rows) // 20):
    raise Invalid("must return 1 row to 5% of rows")
  mine = st.median(D.d(D.rows[j]) for j in got)
  dumb = st.mean(st.median(D.d(r) for r in rnd.sample(D.rows, len(got)))
                 for _ in range(20))
  return clip(1 - mine / dumb)


def q_guess(f, D, rnd):
  k, qs = D.goal[0], []
  for _ in range(SPLITS):
    s = rnd.sample(D.rows, min(len(D.rows), 600))
    cut = len(s) * 5 // 6
    train, test = s[:cut], s[cut:]
    got = list(f(D.header[:], copy(train), [D.hide(r) for r in test]))
    if len(got) != len(test): raise Invalid("one number per test row")
    err = st.mean(abs(float(g) - r[k]) for g, r in zip(got, test))
    mu = st.mean(r[k] for r in train)
    qs.append(1 - err / (st.mean(abs(mu - r[k]) for r in test) + 1e-32))
  return clip(st.mean(qs))


def q_certify(f, D, rnd):
  shapes = [(lambda: rnd.gauss(0, 1), 1), (lambda: rnd.random(), 12 ** -.5),
            (lambda: rnd.expovariate(1), 1)]
  hit = {True: 0, False: 0}
  for j in range(PAIRS):
    gen, sd = shapes[j % 3]
    n = (10, 30, 100)[(j // 3) % 3]
    same = j % 2 == 0
    shift = 0 if same else (.5, 1, 2)[(j // 2) % 3] * sd
    xs, ys = [gen() for _ in range(n)], [gen() + shift for _ in range(n)]
    hit[same] += bool(f(xs, ys)) == same
  return (hit[True] + hit[False]) / PAIRS       # classes are balanced


def q_flow(f, D, rnd):
  pool, qs = rnd.sample(D.rows, min(100, len(D.rows))), []
  avg = st.mean(D.d(r) for r in pool)
  for _ in range(ORDERS):
    rnd.shuffle(pool)
    pick = pool[-1]                              # never chose: stuck with last
    for j, row in enumerate(pool):
      if f(D.header[:], row[:], copy(pool[:j])):
        pick = row; break
    qs.append(1 - D.d(pick) / avg)
  return clip(st.mean(qs))


def q_blame(f, D, rnd):
  names = [D.header[k] for k in D.x]
  got = list(dict.fromkeys(f(D.header[:], copy(D.rows))))
  if not got or any(g not in names for g in got):
    raise Invalid("must name one or more input columns")
  by = sorted(D.rows, key=D.d)
  best, worst = by[:len(by) // 4], by[-len(by) // 4:]
  good = {k: (st.median(r[k] for r in best) if D.num[k] else
              st.mode(r[k] for r in best)) for k in D.x}
  guess = D.oracle(rnd.sample(D.rows, min(600, len(D.rows))))
  bad = rnd.sample(worst, min(30, len(worst)))
  old = st.mean(guess(r) for r in bad)
  def gain(cols):
    ks = [D.header.index(c) for c in cols]
    new = st.mean(guess([(good[k] if k in ks else v)
                         for k, v in enumerate(r)]) for r in bad)
    return (old - new) / (old + 1e-32)
  dumb = st.mean(gain(rnd.sample(names, len(got))) for _ in range(10))
  return clip(gain(got) - dumb)


def q_justify(f, D, rnd):
  by = sorted(D.rows, key=D.d)
  rank = {id(r): j for j, r in enumerate(by)}
  mine = dumb = 0
  for row in rnd.sample(by[:len(by) // 4], 20):
    truth = 1 - rank[id(row)] / (len(by) - 1)
    p, why = f(D.header[:], copy(D.rows), D.hide(row))
    if not isinstance(why, str) or not why.strip():
      raise Invalid("no reason given")
    mine += abs(float(p) - truth)
    dumb += abs(.5 - truth)
  return clip((dumb - mine) / dumb)


def q_choose(f, D, rnd):
  qs = []
  for _ in range(RUNS):
    pool = rnd.sample(D.rows, min(POOL, len(D.rows)))
    got = indices([f(D.header[:], [D.hide(r) for r in pool],
                     labeller(D, pool))], len(pool))
    qs.append(versus_random(D, pool, got[0], rnd))
  return st.mean(qs)


def q_fix(f, D, rnd):
  by, ok = sorted(D.rows, key=D.d), 0
  for row in rnd.sample(by[-len(by) // 4:], 20):
    try:
      got = f(D.header[:], row[:], dict(D.levers))
      good = isinstance(got, dict) and len(got) > 0
      for name, v in (got.items() if good else []):
        allowed = D.levers.get(name)
        if allowed is None: good = False
        elif isinstance(allowed, tuple):
          good &= (isinstance(v, (int, float)) and not isinstance(v, bool)
                   and allowed[0] <= v <= allowed[1])
        else: good &= v in allowed
      good = good and any(row[D.header.index(n)] != v for n, v in got.items())
      ok += bool(good)
    except Exception: pass                       # that row gets no credit
  return ok / 20


def q_spot(f, D, rnd):
  nums, qs = [k for k in D.x if D.num[k] and D.sd[k] > 0], []
  if not nums: raise Invalid("no numeric input column to corrupt")
  for _ in range(COPIES):
    rows = copy(rnd.sample(D.rows, min(1000, len(D.rows))))
    wrong = rnd.sample(range(len(rows)), INJECT)
    for j in wrong:
      k = rnd.choice(nums)
      rows[j][k] = D.mu[k] + rnd.choice((-1, 1)) * 6 * D.sd[k]
    got = indices(f(D.header[:], copy(rows)), len(rows))[:TOP]
    qs.append(sum(j in wrong for j in got) / TOP)
  return st.mean(qs)


def q_race(f, D, rnd):
  qs = []
  for _ in range(RUNS):
    pool = rnd.sample(D.rows, min(POOL, len(D.rows)))
    try:
      got = f(D.header[:], [D.hide(r) for r in pool], labeller(D, pool))
      tried = {str(t).lower() for t in got["tried"]}
      if len(tried) < 3 or "random" not in tried:
        raise Invalid("needs three strategies, one named random")
      row = indices([got["row"]], len(pool))[0]
      qs.append(versus_random(D, pool, row, rnd))
    except Exception: qs.append(0)               # an invalid race has failed
  return st.mean(qs)


SCORERS = dict(remember=q_remember, guess=q_guess, certify=q_certify,
               flow=q_flow, blame=q_blame, justify=q_justify, choose=q_choose,
               fix=q_fix, spot=q_spot, race=q_race)


# -- child: grade one program ------------------------------------------
def child(file, skill, data, levers):
  "Import FILE, call its skill function, print Q as the last line."
  file = Path(file).resolve()
  os.chdir(file.parent)
  sys.path.insert(0, str(file.parent))
  seed = zlib.crc32(f"{Path(data).name}/{skill}".encode())
  random.seed(seed)
  D = Data(data, json.loads(levers))
  with contextlib.redirect_stdout(io.StringIO()):
    spec = importlib.util.spec_from_file_location(file.stem, file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    f = getattr(mod, skill, None)
    if not callable(f): raise Invalid(f"no function named {skill}")
    q = SCORERS[skill](f, D, random.Random(seed))
  print("@@Q " + json.dumps(float(q)))


# -- parent: grade them all ---------------------------------------------
def grade(cfg, call, timeout):
  "Score one logged call. Any failure earns the baseline."
  d = run.ROOT / call["dir"] if not Path(call["dir"]).is_absolute() \
      else Path(call["dir"])
  skill, dom = call["skill"], cfg["domains"][call["domain"]]
  out = dict(domain=call["domain"], treatment=call["treatment"],
             trial=call["trial"], step=call["step"], skill=skill,
             q=BASELINE[skill], status="no_code", detail="", secs=0,
             dir=call["dir"])
  file = d / f"step{int(call['step']):02d}.py"
  if file.exists():
    t = time.time()
    try:
      r = subprocess.run(
        [sys.executable, str(RIG / "score.py"), "--one", str(file), skill,
         str(run.ROOT / dom["data"]), json.dumps(dom.get("levers", []))],
        capture_output=True, text=True, encoding="utf8", errors="replace",
        timeout=timeout, env=dict(os.environ, PYTHONUTF8="1"))
      last = [s for s in r.stdout.splitlines() if s.startswith("@@Q ")]
      if r.returncode == 0 and last:
        out.update(q=round(json.loads(last[-1][4:]), 4), status="ok")
      else:
        tail = (r.stderr.strip().splitlines() or ["no output"])[-1]
        out.update(status="invalid" if "Invalid" in tail else "error",
                   detail=tail[:200])
    except subprocess.TimeoutExpired:
      out.update(status="timeout", detail=f"over {timeout} s")
    out["secs"] = round(time.time() - t, 1)
  with LOCK:
    log = cfg["scores"]
    new = not log.exists()
    with open(log, "a", newline="", encoding="utf8") as fh:
      w = csv.DictWriter(fh, FIELDS)
      if new: w.writeheader()
      w.writerow(out)
  return out


def main():
  if len(sys.argv) > 1 and sys.argv[1] == "--one":
    return child(*sys.argv[2:6])
  ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
  ap.add_argument("--config")
  ap.add_argument("--workers", type=int, default=4)
  ap.add_argument("--timeout", type=int, default=300)
  a = ap.parse_args()
  cfg = run.load_config(a.config)
  cfg["scores"] = cfg["log"].with_name("scores.csv")
  if not cfg["log"].exists(): sys.exit(f"nothing to score: no {cfg['log']}")
  calls = list(csv.DictReader(open(cfg["log"], encoding="utf8")))
  done = ({r["dir"] for r in csv.DictReader(open(cfg["scores"],
           encoding="utf8"))} if cfg["scores"].exists() else set())
  todo = [c for c in calls if c["dir"] not in done]
  print(f"{len(todo)} programs to score ({len(done)} already done)")
  with ThreadPoolExecutor(a.workers) as ex:
    res = list(ex.map(lambda c: grade(cfg, c, a.timeout), todo))
  for s in sorted({r["status"] for r in res}):
    print(f"  {s:8} {sum(r['status'] == s for r in res)}")


if __name__ == "__main__":
  main()
