#!/usr/bin/env python3
"""
test_t7.py: checks for the treatment-7 plumbing (rig/t7.py). No LLM.

  python rig/test_t7.py      # want: "failures: 0"

The two tiny skill files below are test fixtures only, written to a
temporary folder and deleted. They are not treatment 7, which must be
written by hand in t7/.
"""
import csv, json, random, shutil, subprocess, sys, tempfile
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
import run, t7

fails = 0
def check(name, ok):
  global fails
  fails += not ok
  print(("pass  " if ok else "FAIL  ") + name)

STEP1 = ("import statistics as st\n\ndef remember(header, rows):\n"
         "    g = header.index('Cost-')\n"
         "    by = sorted(range(len(rows)), key=lambda j: rows[j][g])\n"
         "    return by[:max(1, len(rows) // 20)]\n")
STEP2 = ("from step01 import remember\nimport statistics as st\n\n"
         "def certify(xs, ys):\n"
         "    return abs(st.mean(xs) - st.mean(ys)) < 0.3\n\n"
         "if __name__ == '__main__':\n    print(certify([1, 2], [1, 2]))\n")

tmp = Path(tempfile.mkdtemp(prefix="t7test_"))
try:
  rnd = random.Random(5)
  lines = ["Size,kind,Cost-"] + [f"{rnd.random():.3f},{rnd.choice('ab')},"
                                 f"{rnd.random():.3f}" for _ in range(300)]
  (tmp / "toy.csv").write_text("\n".join(lines) + "\n")
  (tmp / "req.md").write_text("| 1 | Show me the good ones. | remember |\n"
                              "| 2 | Is it real? | certify |\n"
                              "| 3 | Guess. | guess |\n")
  cfg = dict(run.load_config())
  cfg.update(runs=tmp / "runs", log=tmp / "results" / "calls.csv",
             asks=[1, 2, 3], max_rows=None, prompt_version=3,
             domains={"toy": {"data": str(tmp / "toy.csv"),
                              "requirements": str(tmp / "req.md"),
                              "levers": ["Size"]}})
  (tmp / "t7" / "toy").mkdir(parents=True)
  (tmp / "t7" / "toy" / "step01.py").write_text(STEP1)
  (tmp / "t7" / "toy" / "step02.py").write_text(STEP2)
  (tmp / "t7" / "minutes.csv").write_text("domain,step,minutes\ntoy,1,25\n")
  (tmp / "t7" / "shared").mkdir()
  (tmp / "t7" / "shared" / "mylib.py").write_text("def half(x):\n    return x / 2\n")

  out = t7.register(cfg, root=tmp)
  R = list(csv.DictReader(open(cfg["log"], encoding="utf8")))
  check("registers the steps that exist, stops at the first gap",
        [r["step"] for r in R] == ["1", "2"])
  check("rows are treatment 7, with lines counted",
        all(r["treatment"] == "7" for r in R)
        and int(R[0]["new_lines"]) == run.code_lines(STEP1)
        and int(R[1]["total_lines"]) == run.code_lines(STEP1) + run.code_lines(STEP2))
  check("each step has its own folder, so scores never collide",
        len({r["dir"] for r in R}) == 2)
  s2 = cfg["runs"] / "toy" / "t7" / "trial01" / "step02"
  check("a step's folder holds the earlier steps, ezr.py and t7/shared",
        (s2 / "step01.py").exists() and (s2 / "ezr.py").exists()
        and (s2 / "mylib.py").exists())
  check("a demo that imports an earlier step runs", R[1]["ran_ok"] == "1")
  check("human minutes are logged when given",
        R[0]["human_minutes"] == "25.0" and R[1]["human_minutes"] == "")

  t7.register(cfg, root=tmp)
  R2 = list(csv.DictReader(open(cfg["log"], encoding="utf8")))
  check("registering again replaces the rows instead of adding more",
        len(R2) == 2)

  conf = tmp / "c.json"
  conf.write_text(json.dumps({k: (str(v) if isinstance(v, Path) else v)
                              for k, v in cfg.items()}))
  r = subprocess.run([sys.executable, str(RIG / "score.py"), "--config",
                      str(conf), "--workers", "2"], capture_output=True,
                     text=True, timeout=600)
  S = list(csv.DictReader(open(tmp / "results" / "scores.csv", encoding="utf8")))
  check("score.py grades both T7 programs",
        len(S) == 2 and all(s["status"] == "ok" for s in S))
  (tmp / "results" / "scoring.lock").write_text("123")
  r = subprocess.run([sys.executable, str(RIG / "score.py"), "--config",
                      str(conf)], capture_output=True, text=True, timeout=120)
  check("a second scorer on the same results is refused",
        r.returncode != 0 and "another score.py" in (r.stderr + r.stdout))
  (tmp / "results" / "scoring.lock").unlink()
  r = subprocess.run([sys.executable, str(RIG / "t7.py"), "--config",
                      str(conf), "--check"], capture_output=True, text=True,
                     timeout=300)
  check("--check tests every step's function and passes good ones",
        r.returncode == 0 and r.stdout.count(" ok") == 2)
  r = subprocess.run([sys.executable, str(RIG / "t7.py"), "--config",
                      str(conf), "--demo", "toy", "2"],
                     capture_output=True, text=True, timeout=120)
  check("one command runs one step's demo", r.returncode == 0
        and "True" in r.stdout)
  t7.register(cfg, root=tmp)
  S2 = list(csv.DictReader(open(tmp / "results" / "scores.csv", encoding="utf8")))
  check("re-registering clears old T7 scores so changed files are regraded",
        len(S2) == 0)
finally:
  shutil.rmtree(tmp, ignore_errors=True)

print(f"\nfailures: {fails}")
sys.exit(fails > 0)
