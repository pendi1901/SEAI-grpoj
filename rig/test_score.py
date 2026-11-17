#!/usr/bin/env python3
"""
test_score.py: is the scorer fair? No LLM, no network.

Three stand-in programs are graded on a made-up table whose goals depend
on its inputs in a known way:
  GOOD   a sensible answer for each skill: must beat the baseline;
  DUMB   a random or constant answer: must land near the baseline;
  CRASH  raises: must earn exactly the baseline.

  python rig/test_score.py      # want: "failures: 0"

The GOOD answers below are test fixtures written by an LLM. Do not copy
them into treatment 7, which must be written by hand.
"""
import json, random, shutil, subprocess, sys, tempfile
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
from contract import BASELINE, CONTRACT
import run

GOOD = r'''
import random, statistics as st
def _goals(h): return [k for k, c in enumerate(h) if c[-1] in "+-"]
def _xs(h): return [k for k, c in enumerate(h) if c[-1] not in "+-"]
def _d(h, r):
    return sum(r[k] if h[k][-1] == "-" else -r[k] for k in _goals(h))
def remember(header, rows):
    by = sorted(range(len(rows)), key=lambda j: _d(header, rows[j]))
    return by[:max(1, len(rows) // 20)]
def guess(header, train, test):
    g = _goals(header)[0]; a = header.index("A")
    n = len(train); mx = sum(r[a] for r in train) / n
    my = sum(r[g] for r in train) / n
    b = (sum((r[a] - mx) * (r[g] - my) for r in train) /
         sum((r[a] - mx) ** 2 for r in train))
    return [my + b * (r[a] - mx) for r in test]
def certify(xs, ys):
    sd = (st.pvariance(xs) / 2 + st.pvariance(ys) / 2) ** .5
    return abs(st.mean(xs) - st.mean(ys)) <= .35 * sd
def flow(header, row, seen):
    if len(seen) < 30: return False
    return _d(header, row) <= min(_d(header, r) for r in seen)
def blame(header, rows): return ["A"]
def justify(header, rows, row):
    a = header.index("A")
    return sum(r[a] > row[a] for r in rows) / len(rows), "it has a low A"
def _best(header, rows, label):
    a = header.index("A")                     # label the 50 most promising
    top = sorted(range(len(rows)), key=lambda j: rows[j][a])[:50]
    def score(j):
        r = rows[j][:]
        for k, v in zip(_goals(header), label(j)): r[k] = v
        return _d(header, r)
    return min(top, key=score)
def choose(header, rows, label): return _best(header, rows, label)
def fix(header, row, levers):
    name, allowed = next(iter(levers.items()))
    if isinstance(allowed, tuple):
        v = allowed[0] if row[header.index(name)] != allowed[0] else allowed[1]
    else:
        v = next(x for x in allowed if x != row[header.index(name)])
    return {name: v}
def spot(header, rows):
    ks = [k for k in _xs(header) if header[k][0].isupper()]
    mu = {k: st.mean(r[k] for r in rows) for k in ks}
    sd = {k: st.pstdev(r[k] for r in rows) for k in ks}
    z = lambda r: max(abs(r[k] - mu[k]) / sd[k] for k in ks)
    return sorted(range(len(rows)), key=lambda j: -z(rows[j]))[:20]
def race(header, rows, label):
    return dict(winner="lowA", tried=["lowA", "random", "first"],
                row=_best(header, rows, label))
'''

DUMB = r'''
import random
def remember(header, rows): return random.sample(range(len(rows)), len(rows) // 20)
def guess(header, train, test):
    g = [k for k, c in enumerate(header) if c[-1] in "+-"][0]
    return [sum(r[g] for r in train) / len(train)] * len(test)
def certify(xs, ys): return random.random() < .5
def flow(header, row, seen): return random.random() < .05
def blame(header, rows): return ["noise"]
def justify(header, rows, row): return .5, "no idea"
def choose(header, rows, label): return random.randrange(len(rows))
def fix(header, row, levers): return {"A": 1e9}
def spot(header, rows): return random.sample(range(len(rows)), 20)
def race(header, rows, label): return dict(winner="x", tried=["x"], row=0)
'''

CRASH = "\n".join(f"def {s}(*a): raise ValueError('boom')" for s in BASELINE)

fails = 0
def check(name, ok):
  global fails
  fails += not ok
  print(("pass  " if ok else "FAIL  ") + name)


def grade(file, skill, data):
  "Returns (Q, status, number of test cases)."
  r = subprocess.run([sys.executable, str(RIG / "score.py"), "--one",
                      str(file), skill, str(data[0]), str(data[1]),
                      json.dumps(["B", "kind"])],
                     capture_output=True, text=True, timeout=300)
  q = [s for s in r.stdout.splitlines() if s.startswith("@@Q ")]
  if not q: return None, r.stderr[-300:], 0
  res = json.loads(q[-1][4:])
  return sum(res["cases"]) / len(res["cases"]), res["status"], len(res["cases"])


tmp = Path(tempfile.mkdtemp(prefix="scoretest_"))
try:
  rnd = random.Random(7)
  lines = ["A,B,noise,kind,Cost-,Gain+"]
  for _ in range(600):                 # Cost rises with A; Gain falls with A
    a, b, n = rnd.random(), rnd.random(), rnd.random()
    lines.append(f"{a:.4f},{b:.4f},{n:.4f},{rnd.choice('xyz')},"
                 f"{10*a + rnd.gauss(0, .5):.3f},{5 - 4*a + rnd.gauss(0, .3):.3f}")
  data = tmp / "toy.csv"
  data.write_text("\n".join(lines) + "\n")
  cfg = dict(domains=dict(toy=dict(data=str(data))))
  data = run.split(cfg, "toy")                 # (train 80%, test 20%)
  n_train = len(data[0].read_text().splitlines()) - 1
  n_test = len(data[1].read_text().splitlines()) - 1
  check("split is 80/20 and loses no rows", (n_train, n_test) == (480, 120))
  check("split is repeatable", run.split(cfg, "toy") == data)
  for name, text in (("good", GOOD), ("dumb", DUMB), ("crash", CRASH)):
    (tmp / f"{name}.py").write_text(text)

  check("every skill has a contract, a baseline and a scorer",
        set(CONTRACT) == set(BASELINE))
  print(f"\n{'skill':9} {'base':>5} {'good':>6} {'dumb':>6}")
  for skill, base in BASELINE.items():
    good, e1, n1 = grade(tmp / "good.py", skill, data)
    dumb, e2, n2 = grade(tmp / "dumb.py", skill, data)
    crash, e3, n3 = grade(tmp / "crash.py", skill, data)
    show = lambda v: "fail" if v is None else f"{v:.2f}"
    print(f"{skill:9} {base:5.2f} {show(good):>6} {show(dumb):>6}")
    if good is None or e1 != "ok": print("   ", e1)
    check(f"{skill}: a good answer beats the baseline",
          good is not None and good > base + .1)
    check(f"{skill}: a dumb answer does not",
          dumb is None or dumb < base + .1)
    check(f"{skill}: a crash earns the baseline on every test case",
          crash == base and n3 > 0)
finally:
  shutil.rmtree(tmp, ignore_errors=True)

print(f"\nfailures: {fails}")
sys.exit(fails > 0)
