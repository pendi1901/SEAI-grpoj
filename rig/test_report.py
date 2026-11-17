#!/usr/bin/env python3
"""
test_report.py: checks for report.py on made-up logs. No LLM, no network.

  python rig/test_report.py     # want: "failures: 0"
"""
import csv, json, random, shutil, subprocess, sys, tempfile
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
import report, run, score

fails = 0
def check(name, ok):
  global fails
  fails += not ok
  print(("pass  " if ok else "FAIL  ") + name)

rnd = random.Random(1)
bag = lambda mu, n=30: [rnd.gauss(mu, 1) for _ in range(n)]

# -- same and ranks, against the course's own demo (ezr-eg6 --ranks) ----
a = bag(10)
d = dict(a=a, b=[x + rnd.gauss(0, .02) for x in a],
         c=[x + 1.5 for x in a], d=[x + 4 for x in a])
r = report.ranks(d)
check("ties share rank 0", r["a"] == 0 and r["b"] == 0)
check("a real gap gets a new rank", r["c"] == 1 and r["d"] == 2)
check("big=True reverses the order", report.ranks(d, big=True)["d"] == 0)
b = dict(lo=[1] * 67 + [0] * 33, hi=[1] * 88 + [0] * 12, mid=[1] * 83 + [0] * 17)
r = report.ranks(b, big=True)
check("0/1 data: equal medians are ordered by mean, best first",
      r["hi"] == 0 and r["mid"] == 0 and r["lo"] == 1)
check("same: a sample equals itself", report.same(a, a))
check("same: constant lists that differ are different",
      not report.same([5, 5, 5], [9, 9, 9]))
check("same: identical constant lists are the same",
      report.same([5, 5, 5], [5, 5, 5]))

# -- a full report on synthetic logs -----------------------------------
tmp = Path(tempfile.mkdtemp(prefix="reporttest_"))
try:
  calls, scores = [], []
  for t, reuse in (("1", 0), ("2", 1)):
    for trial in range(1, 11):
      total = 0
      for step, skill in enumerate(run.SKILLS[:4], 1):
        # T1 writes ~100 lines every step; T2's new code falls away.
        new = int(rnd.gauss(100, 5)) if not reuse else int(rnd.gauss(100 / step ** 2, 2))
        total += new
        dir_ = f"runs/toy/t{t}/trial{trial:02d}/step{step:02d}"
        calls.append(dict(domain="toy", treatment=t, reuse=reuse, trial=trial,
                          step=step, skill=skill, new_lines=new,
                          total_lines=total, pct_new=round(100 * new / total, 1),
                          got_code=1, dir=dir_))
        q = rnd.gauss(.6 if reuse else .2, .05)       # T2 also scores higher
        scores.append(dict(dir=dir_, q=q, status="ok"))
  def dump(name, rows):
    with open(tmp / name, "w", newline="", encoding="utf8") as f:
      w = csv.DictWriter(f, list(rows[0])); w.writeheader(); w.writerows(rows)
  dump("calls.csv", calls); dump("scores.csv", scores)
  cfg = json.loads((RIG / "config.json").read_text("utf8"))
  cfg.update(log=str(tmp / "calls.csv"))
  (tmp / "c.json").write_text(json.dumps(cfg))
  r = subprocess.run([sys.executable, str(RIG / "report.py"), "--config",
                      str(tmp / "c.json")], capture_output=True, text=True)
  check("report runs", r.returncode == 0)
  if r.returncode: print(r.stderr[-600:])
  md = (tmp / "report.md").read_text("utf8")
  check("figure written", (tmp / "fig" / "toy.png").stat().st_size > 5000)
  rows = {l.split("|")[1].strip(): [c.strip() for c in l.split("|")[2:-1]]
          for l in md.split("### New lines of code per step")[1]
                     .split("###")[0].splitlines() if l.startswith("| T")}
  check("step 1: both treatments tie on new lines",
        rows["T1 plain"][0].endswith("(0)") and
        rows["T2 plain+reuse"][0].endswith("(0)"))
  check("step 4: the reuse treatment wins on new lines",
        rows["T2 plain+reuse"][3].endswith("(0)") and
        rows["T1 plain"][3].endswith("(1)"))
  ztab = md.split("## All domains together")[1].split("New lines, pooled")[0]
  first = [l for l in ztab.splitlines() if l.startswith("| T")][0]
  check("pooled Z ranks the better-scoring treatment first",
        first.startswith("| T2") and first.rstrip(" |").endswith("0"))
  cs = report.load(dict(log=tmp / "calls.csv")); report.add_z(cs)
  z = [c["z"] for c in cs if c["skill"] == "remember"]
  check("Z has mean 0 and sd 1 within a skill",
        abs(sum(z) / len(z)) < 1e-9 and abs(sum(v * v for v in z) / len(z) - 1) < 1e-9)
finally:
  shutil.rmtree(tmp, ignore_errors=True)

print(f"\nfailures: {fails}")
sys.exit(fails > 0)
