#!/usr/bin/env python3
"""
run.py: climb the skill ladder with an LLM, many times, and log every call.

One CLIMB = one (domain, treatment, trial): ten LLM calls in order, where
call i is given the code from calls 1..i-1 of the same climb. Different
climbs share nothing, so they can run side by side.

  python rig/run.py fetch                 # download the data and ezr.py
  python rig/run.py plan                  # show what would run
  python rig/run.py go --limit 10         # timing test: ten calls only
  python rig/run.py go --trials 3 --workers 8
  python rig/run.py status                # done so far, mean seconds, ETA

Everything is resumable: a finished call leaves done.json in its directory
and is never repeated. Written with LLM help (see rig/README.md); this is
experiment tooling and is not part of the hand-written treatment 7.
"""
import argparse, csv, json, re, shutil, subprocess, sys, threading, time
import os, zlib
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RIG = ROOT / "rig"
SKILLS = "remember guess certify flow blame justify choose fix spot race".split()

# uproj.md says both "supply the code for skills 1..i" in every treatment
# and "ask for each skill cold". Reading used here: the no-reuse treatments
# still see the earlier code but are not told to reuse it. Set this False
# if the lecturer says they should see nothing (open question 6).
SHOW_PRIOR_TO_NO_REUSE = True

LIB_TEXT = {
  "plain": "Use only the Python standard library.",
  "sklearn": "You may use scikit-learn, numpy and pandas.",
  "ezr": "The file ezr.py is in this directory. Its source is shown "
         "below. Build on it: `import ezr`.",
}
FIELDS = ("when domain data treatment library reuse trial step skill ask "
          "backend model dir new_lines total_lines pct_new got_code ran_ok "
          "llm_secs run_secs prompt_chars reply_chars prompt_tokens "
          "reply_tokens seed error").split()
LOCK = threading.Lock()


def load_config(path=None):
  "Read the config, resolving its paths against the repo root."
  cfg = json.loads(Path(path or RIG / "config.json").read_text("utf8"))
  cfg["runs"] = ROOT / cfg.get("runs", "runs")
  cfg["log"] = ROOT / cfg.get("log", "results/calls.csv")
  return cfg


def asks(cfg, domain):
  "The asks chosen for this domain's ladder: [(number, text, skill)]."
  d = cfg["domains"][domain]
  rows = []
  for line in (ROOT / d["requirements"]).read_text("utf8").splitlines():
    m = re.match(r"\|\s*(\d+)\s*\|(.+)\|\s*(\w+)\s*\|\s*$", line)
    if m and m[3] in SKILLS:
      rows.append((int(m[1]), m[2].strip(), m[3]))
  want = d.get("asks") or cfg["asks"]
  picked = [r for n in want for r in rows if r[0] == n]
  if len(picked) != len(want):
    sys.exit(f"{domain}: asked for asks {want}, found {len(picked)} of them")
  return picked


def code_lines(text):
  "Lines that are neither blank nor only a comment."
  return sum(1 for s in text.splitlines()
             if s.strip() and not s.strip().startswith("#"))


def extract_code(reply):
  "The longest fenced block in the reply, or None."
  blocks = re.findall(r"```(?:python|py)?[ \t]*\n(.*?)```", reply, re.S)
  return max(blocks, key=len).strip() + "\n" if blocks else None


def build_prompt(cfg, domain, treat, step, ask, prior, data_path):
  "Background library + earlier skills + the one-line ask."
  lib, reuse = treat["library"], treat["reuse"]
  head = data_path.read_text("utf8").splitlines()[:4]
  p = [f"You are writing one Python file, step{step:02d}.py.",
       "",
       f"The data is the csv file {data_path.name} in the current "
       "directory. Column names starting in upper case are numeric, lower "
       "case are symbolic. A name ending in - is a goal to minimise, in + "
       "a goal to maximise; all other columns are inputs. Its first lines:",
       "", *head, "",
       LIB_TEXT[lib]]
  if lib == "ezr":
    p += ["", "--- ezr.py ---", (RIG / "lib" / "ezr.py").read_text("utf8")]
  if prior and (reuse or SHOW_PRIOR_TO_NO_REUSE):
    p += ["", "These files, written earlier, are in the same directory:"]
    for name, text in prior:
      p += ["", f"--- {name} ---", text]
  if reuse and prior:
    p += ["", "Reuse the earlier files wherever you can: import from them "
              "rather than rewriting. Write as little new code as possible. "
              "Do not edit the earlier files."]
  p += ["", "The customer asks:", "", f"  {ask}", "",
        f"Write step{step:02d}.py to answer that ask on this data. Running "
        f"`python step{step:02d}.py` must print a short answer a customer "
        "could read, and exit with status 0. Reply with the complete file "
        "in one ```python fenced block and nothing else."]
  return "\n".join(p)


def claude_md_above(path):
  "Any CLAUDE.md at or above PATH: it would leak context into a trial."
  return [str(d / "CLAUDE.md") for d in [path, *path.parents]
          if (d / "CLAUDE.md").exists()]


def call_ollama(b, prompt, seed):
  """One stateless call to a local Ollama server. No `context` is sent, so
  the model sees this prompt and nothing else. Returns (reply, meta)."""
  opts = dict(b.get("options", {}), seed=seed)
  body = dict(model=b["model"], prompt=prompt, stream=False, options=opts)
  if "think" in b: body["think"] = b["think"]     # reasoning models only
  body = json.dumps(body).encode()
  req = urllib.request.Request(b["url"].rstrip("/") + "/api/generate", body,
                               {"Content-Type": "application/json"})
  with urllib.request.urlopen(req, timeout=b.get("timeout", 900)) as r:
    out = json.loads(r.read())
  return out.get("response", ""), dict(
    prompt_tokens=out.get("prompt_eval_count", 0),
    reply_tokens=out.get("eval_count", 0),
    ctx=opts.get("num_ctx", 0))


def call_llm(cfg, prompt, cwd, seed=0):
  "Send PROMPT to the backend. Returns (reply, seconds, meta)."
  b = cfg["backends"][cfg["backend"]]
  if "url" in b:
    t = time.time()
    reply, meta = call_ollama(b, prompt, seed)
    return reply, time.time() - t, meta
  cmd = [c.replace("{rig}", str(RIG)).replace("{python}", sys.executable)
         for c in b["cmd"]]
  cmd[0] = shutil.which(cmd[0]) or cmd[0]
  t = time.time()
  r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                     encoding="utf8", errors="replace", cwd=cwd,
                     timeout=b.get("timeout", 600))
  if r.returncode != 0:
    raise RuntimeError(f"backend exit {r.returncode}: {r.stderr[-300:]}")
  return r.stdout, time.time() - t, {}


def smoke(cfg, d, name):
  "Does the new file run at all? Not a quality score; see the scorer."
  t = time.time()
  try:
    # PYTHONUTF8: else printing a non-ASCII character such as a
    # greater-or-equal sign crashes on a Windows console code page,
    # and the rig would blame the generated program for it.
    r = subprocess.run([sys.executable, name], cwd=d, capture_output=True,
                       env=dict(os.environ, PYTHONUTF8="1"),
                       text=True, encoding="utf8", errors="replace",
                       timeout=cfg.get("run_timeout", 120))
    (d / "run.out").write_text(r.stdout[-5000:] + "\n--- stderr ---\n"
                               + r.stderr[-5000:], "utf8")
    return r.returncode == 0, time.time() - t
  except subprocess.TimeoutExpired:
    (d / "run.out").write_text("TIMEOUT", "utf8")
    return False, time.time() - t


def log_row(cfg, row):
  "Append one row to the csv the moment a call ends."
  with LOCK:
    cfg["log"].parent.mkdir(parents=True, exist_ok=True)
    new = not cfg["log"].exists()
    with open(cfg["log"], "a", newline="", encoding="utf8") as f:
      w = csv.DictWriter(f, FIELDS)
      if new: w.writeheader()
      w.writerow(row)


def one_call(cfg, domain, tid, trial, step, ask, prior):
  "One LLM call in its own fresh directory. Returns the new file's text."
  treat = cfg["treatments"][tid]
  dom = cfg["domains"][domain]
  d = cfg["runs"] / domain / f"t{tid}" / f"trial{trial:02d}" / f"step{step:02d}"
  name = f"step{step:02d}.py"
  if (d / "done.json").exists():                       # resume
    return (d / name).read_text("utf8") if (d / name).exists() else ""
  if d.exists(): shutil.rmtree(d)                      # half-finished: redo
  d.mkdir(parents=True)
  leaks = claude_md_above(d)
  if leaks: sys.exit(f"CLAUDE.md would leak into trials: {leaks}")
  data = ROOT / dom["data"]
  shutil.copy(data, d / data.name)
  if treat["library"] == "ezr": shutil.copy(RIG / "lib" / "ezr.py", d)
  for pname, ptext in prior: (d / pname).write_text(ptext, "utf8")

  b = cfg["backends"][cfg["backend"]]
  prompt = build_prompt(cfg, domain, treat, step, ask[1], prior, d / data.name)
  (d / "prompt.txt").write_text(prompt, "utf8")
  prior_total = sum(code_lines(t) for _, t in prior)
  seed = zlib.crc32(f"{domain}/{tid}/{trial}/{step}".encode()) % 2**31
  row = dict(when=time.strftime("%Y-%m-%dT%H:%M:%S"), domain=domain,
             data=data.name, treatment=tid, library=treat["library"],
             reuse=int(treat["reuse"]), trial=trial, step=step, skill=ask[2],
             ask=ask[0], backend=cfg["backend"], model=b.get("model", ""),
             dir=(d.relative_to(ROOT) if d.is_relative_to(ROOT) else d
                  ).as_posix(),
             prompt_chars=len(prompt), new_lines=0, total_lines=prior_total,
             pct_new=0, got_code=0, ran_ok=0, llm_secs=0, run_secs=0,
             reply_chars=0, prompt_tokens=0, reply_tokens=0, seed=seed,
             error="")
  code = ""
  try:
    reply, secs, meta = call_llm(cfg, prompt, d, seed)
    row["llm_secs"] = round(secs, 1)
    row.update({k: meta[k] for k in ("prompt_tokens", "reply_tokens")
                if k in meta})
    if meta.get("ctx") and meta.get("prompt_tokens", 0) >= .95 * meta["ctx"]:
      row["error"] = "prompt filled the context window: likely truncated"
    (d / "reply.txt").write_text(reply, "utf8")
    row["reply_chars"] = len(reply)
    code = extract_code(reply) or ""
    if code:
      (d / name).write_text(code, "utf8")
      new = code_lines(code)
      row.update(got_code=1, new_lines=new, total_lines=prior_total + new,
                 pct_new=round(100 * new / (prior_total + new), 1))
      ok, secs = smoke(cfg, d, name)
      row.update(ran_ok=int(ok), run_secs=round(secs, 1))
    else:
      row["error"] = (row["error"] + "; no fenced code in reply").strip("; ")
  except Exception as e:                    # a failed call is a logged result
    row["error"] = f"{type(e).__name__}: {e}"[:300]
  log_row(cfg, row)
  (d / "done.json").write_text(json.dumps(row, indent=1), "utf8")
  return code


def climb(cfg, domain, tid, trial, budget):
  "All steps of one (domain, treatment, trial), in order."
  prior = []
  for step, ask in enumerate(asks(cfg, domain), 1):
    d = cfg["runs"] / domain / f"t{tid}" / f"trial{trial:02d}" / f"step{step:02d}"
    if not (d / "done.json").exists():
      with LOCK:
        if budget[0] == 0: return
        if budget[0] > 0: budget[0] -= 1
    code = one_call(cfg, domain, tid, trial, step, ask, prior)
    if code: prior.append((f"step{step:02d}.py", code))


def climbs(cfg, a):
  "Every (domain, treatment, trial) selected on the command line."
  doms = a.domains or list(cfg["domains"])
  tids = a.treatments or list(cfg["treatments"])
  n = a.trials or cfg["trials"]
  return [(d, t, k) for k in range(1, n + 1) for d in doms for t in tids]


def cmd_go(cfg, a):
  todo, budget = climbs(cfg, a), [a.limit]
  need = {cfg["treatments"][t]["library"] for _, t, _ in todo}
  if "ezr" in need and not (RIG / "lib" / "ezr.py").exists():
    sys.exit("rig/lib/ezr.py is missing: run `python rig/run.py fetch`")
  for d in {d for d, _, _ in todo}:
    if not (ROOT / cfg["domains"][d]["data"]).exists():
      sys.exit(f"{cfg['domains'][d]['data']} is missing: run fetch")
  print(f"{len(todo)} climbs, backend={cfg['backend']}, workers={a.workers}")
  with ThreadPoolExecutor(a.workers) as ex:
    for f in [ex.submit(climb, cfg, *c, budget) for c in todo]: f.result()
  cmd_status(cfg, a)


def cmd_plan(cfg, a):
  todo = climbs(cfg, a)
  steps = {d: len(asks(cfg, d)) for d in {d for d, _, _ in todo}}
  b = cfg["backends"][cfg["backend"]]
  print(f"backend   {cfg['backend']}: {b.get('url') or b.get('cmd')}")
  print(f"climbs    {len(todo)}")
  print(f"LLM calls {sum(steps[d] for d, _, _ in todo)}")
  for d in sorted(steps):
    print(f"\n{d}: {cfg['domains'][d]['data']}")
    for n, text, skill in asks(cfg, d): print(f"  {n:2} {skill:9} {text[:60]}")


def cmd_status(cfg, a):
  todo = climbs(cfg, a)
  total = sum(len(asks(cfg, d)) for d, _, _ in todo)
  rows = (list(csv.DictReader(open(cfg["log"], encoding="utf8")))
          if cfg["log"].exists() else [])
  n = len(rows)
  if not n: return print(f"0 of {total} calls done")
  secs = sum(float(r["llm_secs"]) + float(r["run_secs"]) for r in rows) / n
  ok = sum(r["ran_ok"] == "1" for r in rows)
  left = max(0, total - n)
  print(f"{n} of {total} calls done; {ok} ran clean ({100*ok//n}%); "
        f"{secs:.0f} s per call")
  print(f"ETA for the other {left}: {left*secs/3600:.1f} h with 1 worker, "
        f"{left*secs/3600/a.workers:.1f} h with {a.workers}")


def cmd_fetch(cfg, a):
  "Download the data sets and ezr.py named in the config."
  for dest, url in cfg["fetch"].items():
    p = ROOT / dest
    if p.exists(): print("have ", dest); continue
    p.parent.mkdir(parents=True, exist_ok=True)
    print("fetch", dest)
    urllib.request.urlretrieve(url, p)


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
  ap.add_argument("cmd", choices=["go", "plan", "status", "fetch"])
  ap.add_argument("--config")
  ap.add_argument("--backend")
  ap.add_argument("--trials", type=int)
  ap.add_argument("--domains", nargs="*")
  ap.add_argument("--treatments", nargs="*")
  ap.add_argument("--workers", type=int, default=1)
  ap.add_argument("--limit", type=int, default=-1,
                  help="stop after this many new calls")
  a = ap.parse_args()
  cfg = load_config(a.config)
  if a.backend: cfg["backend"] = a.backend
  if cfg["backend"] not in cfg["backends"]:
    sys.exit(f"unknown backend {cfg['backend']}")
  {"go": cmd_go, "plan": cmd_plan, "status": cmd_status,
   "fetch": cmd_fetch}[a.cmd](cfg, a)


if __name__ == "__main__":
  main()
