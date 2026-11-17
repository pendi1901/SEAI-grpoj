#!/usr/bin/env python3
"""
score.py: grade every generated program on a fixed test suite.

  python rig/score.py                 # score every call not yet scored
  python rig/score.py --workers 8
  python rig/score.py --config timing/x.json

How each skill is judged is set out, for a human to agree or change, in
docs/assessment.md. In short: each data set is split 80/20 once; skills
work from the 80% and are tested on the 20%; every program for a skill
faces the same test cases; each test case yields one number scaled so
that a no-effort answer earns the skill's baseline; Q is the mean over
test cases; any failure earns the baseline on every case.

Outputs, beside the calls log:
  scores.csv    one row per program: Q and what happened
  cases.jsonl   one line per program: the per-test-case numbers, which
                are what `same` compares across treatments

Each program is graded in its own child process with a time limit.
Written with LLM help; experiment tooling, not part of treatment 7.
"""
import argparse, contextlib, csv, importlib.util, io, json, os, random
import statistics as st, subprocess, sys, threading, time, zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
import run
from contract import BASELINE

FIELDS = "domain treatment trial step skill q n status detail secs dir".split()
LOCK = threading.Lock()

PAIRS, ORDERS, RUNS, BUDGET = 200, 100, 30, 50
COPIES, INJECT, TOP = 10, 10, 20
POOL = 150                 # rows per choose/race run
CAP_TRAIN, CAP_TEST = 2000, 400


class Invalid(Exception):
  "The skill answered, but outside the rules."


def read(path):
  rows = [r for r in csv.reader(open(path, encoding="utf8")) if r]
  return [c.strip() for c in rows[0]], rows[1:]


class Data:
  "Train rows (what skills learn from) and test rows (what they face)."
  def __init__(i, train, test, levers=()):
    i.header, a = read(train)
    _, b = read(test)
    i.num = [c[0].isupper() for c in i.header]
    i.goal = [k for k, c in enumerate(i.header) if c[-1] in "+-"]
    i.x = [k for k, c in enumerate(i.header) if c[-1] not in "+-"]
    cells = lambda rows: [[i.cell(k, v) for k, v in enumerate(r)] for r in rows]
    i.rows, i.test = cells(a), cells(b)
    if len(i.rows) > CAP_TRAIN: i.rows = random.Random(1).sample(i.rows, CAP_TRAIN)
    if len(i.test) > CAP_TEST: i.test = random.Random(2).sample(i.test, CAP_TEST)
    i.lo, i.hi, i.mu, i.sd = {}, {}, {}, {}
    for k, isnum in enumerate(i.num):           # ranges from train only
      if isnum:
        v = [r[k] for r in i.rows if r[k] != "?"]
        i.lo[k], i.hi[k] = min(v), max(v)
        i.mu[k], i.sd[k] = st.mean(v), st.pstdev(v)
    i.levers, i.extra = {}, {}
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
    return max(0, min(1, (v - i.lo[k]) / (i.hi[k] - i.lo[k] + 1e-32)))

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

  def worst(i, n, rnd):
    by = sorted(i.test, key=i.d)
    q = by[-max(1, len(by) // 4):]
    return rnd.sample(q, min(n, len(q)))

  def best(i, n, rnd):
    by = sorted(i.test, key=i.d)
    q = by[:max(1, len(by) // 4)]
    return rnd.sample(q, min(n, len(q)))


def ncases(skill, D):
  "How many test cases a skill faces: needed to fill in a failure."
  return dict(remember=max(1, len(D.test) // 20), guess=len(D.test),
              certify=PAIRS, flow=ORDERS,
              blame=min(30, max(1, len(D.test) // 4)),
              justify=min(20, max(1, len(D.test) // 4)), choose=RUNS,
              fix=min(20, max(1, len(D.test) // 4)), spot=COPIES,
              race=RUNS)[skill]


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


# -- one per skill: (skill's function, data, rng) -> list of case numbers
def q_remember(f, D, rnd):
  got = indices(f(D.header[:], copy(D.test)), len(D.test))
  if not got or len(got) > max(1, len(D.test) // 20):
    raise Invalid("must return 1 row to 5% of rows")
  dumb = st.mean(st.median(D.d(r) for r in rnd.sample(D.test, len(got)))
                 for _ in range(20))
  return [1 - D.d(D.test[j]) / dumb for j in got]


def q_guess(f, D, rnd):
  k = D.goal[0]
  train = D.rows[:1000]
  got = list(f(D.header[:], copy(train), [D.hide(r) for r in D.test]))
  if len(got) != len(D.test): raise Invalid("one number per test row")
  mu = st.mean(r[k] for r in train)
  dumb = st.mean(abs(mu - r[k]) for r in D.test) + 1e-32
  return [1 - abs(float(g) - r[k]) / dumb for g, r in zip(got, D.test)]


def q_certify(f, D, rnd):
  shapes = [(lambda: rnd.gauss(0, 1), 1), (lambda: rnd.random(), 12 ** -.5),
            (lambda: rnd.expovariate(1), 1)]
  out = []
  for j in range(PAIRS):
    gen, sd = shapes[j % 3]
    n = (10, 30, 100)[(j // 3) % 3]
    same = j % 2 == 0
    shift = 0 if same else (.5, 1, 2)[(j // 2) % 3] * sd
    xs, ys = [gen() for _ in range(n)], [gen() + shift for _ in range(n)]
    out.append(int(bool(f(xs, ys)) == same))
  return out


def q_flow(f, D, rnd):
  pool, out = rnd.sample(D.test, min(100, len(D.test))), []
  avg = st.mean(D.d(r) for r in pool)
  for _ in range(ORDERS):
    rnd.shuffle(pool)
    pick = pool[-1]                              # never chose: stuck with last
    for j, row in enumerate(pool):
      if f(D.header[:], row[:], copy(pool[:j])):
        pick = row; break
    out.append(1 - D.d(pick) / avg)
  return out


def q_blame(f, D, rnd):
  names = [D.header[k] for k in D.x]
  got = list(dict.fromkeys(f(D.header[:], copy(D.rows))))
  if not got or any(g not in names for g in got):
    raise Invalid("must name one or more input columns")
  by = sorted(D.rows, key=D.d)
  top = by[:len(by) // 4]
  good = {k: (st.median(r[k] for r in top) if D.num[k] else
              st.mode(r[k] for r in top)) for k in D.x}
  guess = D.oracle(rnd.sample(D.rows, min(600, len(D.rows))))
  rivals = [rnd.sample(names, len(got)) for _ in range(10)]
  def gain(row, old, cols):
    ks = [D.header.index(c) for c in cols]
    new = guess([(good[k] if k in ks else v) for k, v in enumerate(row)])
    return (old - new) / (old + 1e-32)
  out = []
  for row in D.worst(30, rnd):
    old = guess(row)
    out.append(gain(row, old, got) - st.mean(gain(row, old, c) for c in rivals))
  return out


def q_justify(f, D, rnd):
  ds = sorted(D.d(r) for r in D.rows)
  errs, dumb = [], []
  for row in D.best(20, rnd):
    truth = sum(v > D.d(row) for v in ds) / len(ds)
    p, why = f(D.header[:], copy(D.rows), D.hide(row))
    if not isinstance(why, str) or not why.strip():
      raise Invalid("no reason given")
    errs.append(abs(float(p) - truth))
    dumb.append(abs(.5 - truth))
  m = st.mean(dumb) + 1e-32
  return [(b - e) / m for e, b in zip(errs, dumb)]


def q_choose(f, D, rnd):
  out = []
  for _ in range(RUNS):
    pool = rnd.sample(D.test, min(POOL, len(D.test)))
    got = indices([f(D.header[:], [D.hide(r) for r in pool],
                     labeller(D, pool))], len(pool))
    out.append(versus_random(D, pool, got[0], rnd))
  return out


def q_fix(f, D, rnd):
  """The course's number: is the change allowed? (It says itself that
  this "does not measure improvement".) So a second list is kept in
  D.extra: allowed AND estimated to lower the row's score, judged from
  its 5 nearest training rows."""
  out, helps, fails = [], [], []
  guess = D.oracle(rnd.sample(D.rows, min(600, len(D.rows))))
  for row in D.worst(20, rnd):
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
      out.append(int(bool(good)))
      new = row[:]
      for n, v in (got.items() if good else []): new[D.header.index(n)] = v
      helps.append(int(bool(good) and guess(new) < guess(row)))
    except Exception as e:                       # that row gets no credit
      out.append(0); helps.append(0); fails.append(e)
  if len(fails) == len(out): raise fails[0]      # never worked: an error
  D.extra = dict(fix_helps=helps)
  return out


def q_spot(f, D, rnd):
  nums, out = [k for k in D.x if D.num[k] and D.sd[k] > 0], []
  if not nums: raise Invalid("no numeric input column to corrupt")
  for _ in range(COPIES):
    rows = copy(rnd.sample(D.test, min(1000, len(D.test))))
    wrong = rnd.sample(range(len(rows)), INJECT)
    for j in wrong:
      k = rnd.choice(nums)
      rows[j][k] = D.mu[k] + rnd.choice((-1, 1)) * 6 * D.sd[k]
    got = indices(f(D.header[:], copy(rows)), len(rows))[:TOP]
    out.append(sum(j in wrong for j in got) / TOP)
  return out


def q_race(f, D, rnd):
  out, fails = [], []
  for _ in range(RUNS):
    pool = rnd.sample(D.test, min(POOL, len(D.test)))
    try:
      got = f(D.header[:], [D.hide(r) for r in pool], labeller(D, pool))
      tried = {str(t).lower() for t in got["tried"]}
      if len(tried) < 3 or "random" not in tried:
        raise Invalid("needs three strategies, one named random")
      row = indices([got["row"]], len(pool))[0]
      out.append(versus_random(D, pool, row, rnd))
    except Exception as e:                       # an invalid race has failed
      out.append(0); fails.append(e)
  if len(fails) == len(out): raise fails[0]      # never worked: an error
  return out


SCORERS = dict(remember=q_remember, guess=q_guess, certify=q_certify,
               flow=q_flow, blame=q_blame, justify=q_justify, choose=q_choose,
               fix=q_fix, spot=q_spot, race=q_race)


# -- child: grade one program ------------------------------------------
def child(file, skill, train, test, levers):
  "Import FILE, call its skill function, print the result as one line."
  file = Path(file).resolve()
  os.chdir(file.parent)
  sys.path.insert(0, str(file.parent))
  seed = zlib.crc32(f"{Path(train).name}/{skill}".encode())
  random.seed(seed)
  D = Data(train, test, json.loads(levers))
  status, detail = "ok", ""
  try:
    with contextlib.redirect_stdout(io.StringIO()):
      spec = importlib.util.spec_from_file_location(file.stem, file)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      f = getattr(mod, skill, None)
      if not callable(f): raise Invalid(f"no function named {skill}")
      cases = [clip(float(v)) for v in SCORERS[skill](f, D, random.Random(seed))]
  except BaseException as e:
    if isinstance(e, KeyboardInterrupt): raise
    status = "invalid" if isinstance(e, Invalid) else "error"
    detail = f"{type(e).__name__}: {e}"[:200]
    cases = [BASELINE[skill]] * ncases(skill, D)
  print("@@Q " + json.dumps(dict(status=status, detail=detail,
                                 cases=[round(v, 4) for v in cases],
                                 extra=D.extra)))


# -- parent: grade them all ---------------------------------------------
DATA = {}
def data_for(cfg, domain):
  with LOCK:
    if domain not in DATA:
      tr, te = run.split(cfg, domain)
      DATA[domain] = (tr, te, Data(tr, te, cfg["domains"][domain].get("levers", [])))
  return DATA[domain]


def grade(cfg, call, timeout):
  "Score one logged call. Any failure earns the baseline on every case."
  d = Path(call["dir"])
  d = d if d.is_absolute() else run.ROOT / d
  skill, dom = call["skill"], cfg["domains"][call["domain"]]
  train, test, D = data_for(cfg, call["domain"])
  res = dict(status="no_code", detail="", cases=None)
  file, t = d / f"step{int(call['step']):02d}.py", time.time()
  if file.exists():
    try:
      r = subprocess.run(
        [sys.executable, str(RIG / "score.py"), "--one", str(file), skill,
         str(train), str(test), json.dumps(dom.get("levers", []))],
        capture_output=True, text=True, encoding="utf8", errors="replace",
        timeout=timeout, env=dict(os.environ, PYTHONUTF8="1"))
      last = [s for s in r.stdout.splitlines() if s.startswith("@@Q ")]
      if last: res = json.loads(last[-1][4:])
      else:
        tail = (r.stderr.strip().splitlines() or ["no output"])[-1]
        res.update(status="error", detail=tail[:200])
    except subprocess.TimeoutExpired:
      res.update(status="timeout", detail=f"over {timeout} s")
  cases = res.get("cases") or [BASELINE[skill]] * ncases(skill, D)
  key = dict(domain=call["domain"], treatment=call["treatment"],
             trial=call["trial"], step=call["step"], skill=skill,
             dir=call["dir"])
  out = dict(key, q=round(st.mean(cases), 4), n=len(cases),
             status=res["status"], detail=res["detail"],
             secs=round(time.time() - t, 1))
  with LOCK:
    new = not cfg["scores"].exists()
    with open(cfg["scores"], "a", newline="", encoding="utf8") as fh:
      w = csv.DictWriter(fh, FIELDS)
      if new: w.writeheader()
      w.writerow(out)
    with open(cfg["cases"], "a", encoding="utf8") as fh:
      extra = res.get("extra") or (
        {"fix_helps": [0] * len(cases)} if skill == "fix" else {})
      fh.write(json.dumps(dict(key, cases=cases, extra=extra)) + "\n")
  return out


def main():
  if len(sys.argv) > 1 and sys.argv[1] == "--one":
    return child(*sys.argv[2:7])
  ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
  ap.add_argument("--config")
  ap.add_argument("--workers", type=int, default=4)
  ap.add_argument("--timeout", type=int, default=300)
  a = ap.parse_args()
  cfg = run.load_config(a.config)
  cfg["scores"] = cfg["log"].with_name("scores.csv")
  cfg["cases"] = cfg["log"].with_name("cases.jsonl")
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
