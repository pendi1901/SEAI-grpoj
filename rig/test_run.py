#!/usr/bin/env python3
"""
test_run.py: checks for run.py, using the mock LLM. No network, no cost.

  python rig/test_run.py        # want: "failures: 0"
"""
import csv, json, shutil, subprocess, sys, tempfile
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
import run

fails = 0
def check(name, ok):
  global fails
  fails += not ok
  print(("pass  " if ok else "FAIL  ") + name)


def sandbox(tmp, asks_md):
  "A tiny world: one data set, one requirements doc, a config."
  (tmp / "data.csv").write_text("Size,kind,Cost-\n1,a,3\n2,b,1\n", "utf8")
  (tmp / "req.md").write_text(asks_md, "utf8")
  cfg = json.loads((RIG / "config.json").read_text("utf8"))
  cfg.update(backend="mock", trials=2, asks=[1, 2, 3],
             runs=str(tmp / "runs"), log=str(tmp / "calls.csv"),
             domains={"toy": {"data": str(tmp / "data.csv"),
                              "requirements": str(tmp / "req.md")}},
             treatments={"1": {"library": "plain", "reuse": False},
                         "2": {"library": "plain", "reuse": True}})
  (tmp / "config.json").write_text(json.dumps(cfg), "utf8")
  return tmp / "config.json"


def go(conf, *extra):
  return subprocess.run([sys.executable, str(RIG / "run.py"), "go",
                         "--config", str(conf), *extra],
                        capture_output=True, text=True)


def rows(tmp):
  return list(csv.DictReader(open(tmp / "calls.csv", encoding="utf8")))


GOOD = ("| 1 | Show me the good ones. | remember |\n"
        "| 2 | Guess the cost. | guess |\n"
        "| 3 | Is it real? | certify |\n")

# -- pure functions ---------------------------------------------------
check("code_lines skips blanks and comments",
      run.code_lines("a=1\n\n# note\n  # more\nb=2\n") == 2)
check("extract_code takes the longest fenced block",
      run.extract_code("x\n```python\na=1\nb=2\n```\ny\n```\nc\n```") ==
      "a=1\nb=2\n")
check("extract_code returns None without a block",
      run.extract_code("sorry") is None)

# -- a full run -------------------------------------------------------
tmp = Path(tempfile.mkdtemp(prefix="rigtest_"))
try:
  conf = sandbox(tmp, GOOD)
  r = go(conf, "--workers", "4")
  check("go exits clean", r.returncode == 0)
  R = rows(tmp)
  check("2 treatments x 2 trials x 3 steps = 12 calls logged", len(R) == 12)
  check("every call got code and ran", all(x["got_code"] == "1" and
                                           x["ran_ok"] == "1" for x in R))
  step1 = [x for x in R if x["step"] == "1"]
  check("step 1 is 100% new", all(float(x["pct_new"]) == 100 for x in step1))
  t1 = [int(x["new_lines"]) for x in R if x["treatment"] == "1" and x["step"] == "3"]
  t2 = [int(x["new_lines"]) for x in R if x["treatment"] == "2" and x["step"] == "3"]
  check("reuse treatment writes fewer new lines", max(t2) < min(t1))
  x = next(x for x in R if x["treatment"] == "2" and x["step"] == "3")
  d = tmp / "runs" / "toy" / "t2" / f"trial{int(x['trial']):02d}" / "step03"
  check("later step's dir holds the earlier files",
        (d / "step01.py").exists() and (d / "step02.py").exists())
  check("total_lines is the running sum",
        int(x["total_lines"]) == sum(run.code_lines((d / f"step0{i}.py")
                                     .read_text()) for i in (1, 2, 3)))
  p = (d / "prompt.txt").read_text()
  check("reuse prompt says reuse and shows earlier code",
        "Reuse the earlier files" in p and "--- step01.py ---" in p)
  p1 = (tmp / "runs/toy/t1/trial01/step03/prompt.txt").read_text()
  check("no-reuse prompt never says reuse", "Reuse" not in p1)
  check("trials are separate directories",
        (tmp / "runs/toy/t1/trial01").exists() and
        (tmp / "runs/toy/t1/trial02").exists())

  # -- resume ---------------------------------------------------------
  go(conf)
  check("a second go repeats nothing", len(rows(tmp)) == 12)
  shutil.rmtree(tmp / "runs/toy/t1/trial02/step03")
  go(conf)
  check("a deleted step is redone, alone", len(rows(tmp)) == 13)

  # -- CLAUDE.md guard ------------------------------------------------
  shutil.rmtree(tmp / "runs/toy/t1/trial02/step03")
  (tmp / "CLAUDE.md").write_text("leak", "utf8")
  r = go(conf)
  check("refuses to run under a CLAUDE.md", r.returncode != 0 and
        "CLAUDE.md" in (r.stderr + r.stdout))
  (tmp / "CLAUDE.md").unlink()
finally:
  shutil.rmtree(tmp, ignore_errors=True)

# -- limit, and failures are logged not dropped -----------------------
tmp = Path(tempfile.mkdtemp(prefix="rigtest_"))
try:
  conf = sandbox(tmp, "| 1 | Fine. | remember |\n"
                      "| 2 | Please CRASH now. | guess |\n"
                      "| 3 | NOCODE today. | certify |\n")
  go(conf, "--limit", "2")
  check("--limit 2 makes exactly two calls", len(rows(tmp)) == 2)
  go(conf)
  R = rows(tmp)
  check("all 12 calls logged despite failures", len(R) == 12)
  check("a crashing program is logged ran_ok=0",
        all(x["ran_ok"] == "0" and x["got_code"] == "1"
            for x in R if x["step"] == "2"))
  check("a reply with no code is logged with an error",
        all(x["got_code"] == "0" and x["error"]
            for x in R if x["step"] == "3"))
finally:
  shutil.rmtree(tmp, ignore_errors=True)

# -- the real requirements docs parse ---------------------------------
cfg = run.load_config()
for dom in cfg["domains"]:
  a = run.asks(cfg, dom)
  check(f"{dom}: ten asks, one per skill, in ladder order",
        [s for _, _, s in a] == run.SKILLS)

print(f"\nfailures: {fails}")
sys.exit(fails > 0)
