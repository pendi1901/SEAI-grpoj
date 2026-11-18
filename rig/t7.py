#!/usr/bin/env python3
"""
t7.py: register treatment 7 (hand-written skills) so it is scored and
reported exactly like the LLM treatments.

  python rig/t7.py                 # register every file in t7/
  python rig/t7.py --demo hr 3     # run one step's demo, one command

Your team writes `t7/<domain>/stepNN.py` by hand, one file per skill, each
defining the same function the LLM treatments must define (see
t7/README.md). This script then, for each domain:

  1. builds one folder per step under the run folder, laid out like an LLM
     climb (`<runs>/<domain>/t7/trial01/stepNN/`), holding that step's
     file, the earlier steps' files, ezr.py and the training data, so
     imports of earlier steps work exactly as they do for T1-T6;
  2. counts new lines per step, and runs each file's own demo;
  3. replaces any earlier treatment-7 rows in the calls log, and drops
     their old scores so `score.py` grades the current files.

Run it again whenever a T7 file changes, then `score.py` and `report.py`.
Optional: `t7/minutes.csv` (domain,step,minutes) records the human time
spent per step; it appears as wall-clock in the report's cost table.

Plumbing only, written with LLM help. It contains no skill code: under
the lecturer's ruling (A21) treatment 7 itself must be written by hand.
"""
import argparse, csv, json, os, shutil, sys, time
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
import run


def minutes(root):
  p = root / "t7" / "minutes.csv"
  if not p.exists(): return {}
  return {(r["domain"], int(r["step"])): float(r["minutes"])
          for r in csv.DictReader(open(p, encoding="utf8"))}


def drop_old(cfg, dirs):
  "Remove earlier T7 rows from the calls log, scores and per-case file."
  log = cfg["log"]
  if log.exists():
    rows = list(csv.DictReader(open(log, encoding="utf8")))
    keep = [r for r in rows if r.get("treatment") != "7"]
    with open(log, "w", newline="", encoding="utf8") as f:
      w = csv.DictWriter(f, run.FIELDS, extrasaction="ignore")
      w.writeheader(); w.writerows(keep)
  sc = log.with_name("scores.csv")
  if sc.exists():
    rows = list(csv.DictReader(open(sc, encoding="utf8")))
    head = list(rows[0]) if rows else None
    keep = [r for r in rows if r["dir"] not in dirs]
    if head:
      with open(sc, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, head); w.writeheader(); w.writerows(keep)
  cp = log.with_name("cases.jsonl")
  if cp.exists():
    lines = [l for l in open(cp, encoding="utf8") if l.strip()]
    keep = [l for l in lines if json.loads(l)["dir"] not in dirs]
    with open(cp, "w", encoding="utf8", newline="\n") as f: f.writelines(keep)


def register(cfg, root=run.ROOT):
  src_root = root / "t7"
  mins, out = minutes(root), []
  for domain in cfg["domains"]:
    src = src_root / domain
    if not src.is_dir(): continue
    steps = run.asks(cfg, domain)
    train, _ = run.split(cfg, domain)
    total, prior = 0, []
    for step, ask in enumerate(steps, 1):
      name = f"step{step:02d}.py"
      if not (src / name).exists(): break      # a ladder stops at its gap
      code = (src / name).read_text("utf8")
      d = cfg["runs"] / domain / "t7" / "trial01" / f"step{step:02d}"
      if d.exists(): shutil.rmtree(d)
      d.mkdir(parents=True)
      try: os.link(train, d / train.name)
      except OSError: shutil.copy(train, d / train.name)
      shutil.copy(RIG / "lib" / "ezr.py", d)
      for pname, ptext in prior + [(name, code)]:
        (d / pname).write_text(ptext, "utf8")
      new = run.code_lines(code)
      total += new
      ok, secs = run.smoke(cfg, d, name)
      rel = (d.relative_to(run.ROOT) if d.is_relative_to(run.ROOT)
             else d).as_posix()          # the scorer resolves from the repo
      out.append(dict(
        when=time.strftime("%Y-%m-%dT%H:%M:%S"), domain=domain,
        data=train.name, treatment="7", library="human", reuse=1, trial=1,
        step=step, skill=ask[2], ask=ask[0], backend="human", model="",
        dir=rel, new_lines=new, total_lines=total,
        pct_new=round(100 * new / total, 1) if total else 0, got_code=1,
        ran_ok=int(ok), llm_secs=0, run_secs=round(secs, 1),
        prompt_chars=0, reply_chars=0, prompt_tokens=0, reply_tokens=0,
        seed=0, attempts=0, prompt_version=cfg.get("prompt_version", 2),
        check_before="", check_after="", repaired=0,
        human_minutes=mins.get((domain, step), ""), error=""))
      prior.append((name, code))
  dirs = {r["dir"] for r in out}
  drop_old(cfg, dirs | {r["dir"] for r in out})
  for r in out: run.log_row(cfg, r)
  return out


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
  ap.add_argument("--config")
  ap.add_argument("--demo", nargs=2, metavar=("DOMAIN", "STEP"),
                  help="run one registered step's demo and show its output")
  a = ap.parse_args()
  cfg = run.load_config(a.config)
  if a.demo:
    dom, step = a.demo[0], int(a.demo[1])
    d = cfg["runs"] / dom / "t7" / "trial01" / f"step{step:02d}"
    if not (d / f"step{step:02d}.py").exists():
      sys.exit(f"not registered: run `python rig/t7.py` first ({d})")
    ok, _ = run.smoke(cfg, d, f"step{step:02d}.py")
    print((d / "run.out").read_text("utf8"))
    sys.exit(0 if ok else 1)
  out = register(cfg)
  if not out:
    sys.exit("no treatment-7 files found under t7/<domain>/stepNN.py")
  by = {}
  for r in out: by.setdefault(r["domain"], []).append(r)
  for dom, rs in by.items():
    print(f"{dom}: {len(rs)} steps, {sum(r['new_lines'] for r in rs)} lines, "
          f"{sum(r['ran_ok'] for r in rs)} demos ran")
  print("now run: python rig/score.py"
        + (f" --config {a.config}" if a.config else "")
        + "   then rig/report.py the same way")


if __name__ == "__main__":
  main()
