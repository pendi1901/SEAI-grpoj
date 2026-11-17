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
  cfg.update(backend="mock", trials=2, asks=[1, 2, 3], repair=False,
             runs=str(tmp / "runs"), log=str(tmp / "calls.csv"),
             domains={"toy": {"data": str(tmp / "data.csv"),
                              "requirements": str(tmp / "req.md")}},
             treatments={"1": {"library": "plain", "reuse": False},
                         "2": {"library": "plain", "reuse": True}})
  (tmp / "config.json").write_text(json.dumps(cfg), "utf8")
  return tmp / "config.json"


def go(conf, *extra):
  return subprocess.run([sys.executable, str(RIG / "run.py"), "go",
                         "--config", str(conf), "--backend",
                         json.loads(conf.read_text())["backend"], *extra],
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
  check("prompt states the file's true row count",
        "It has 2 data rows after the header" in p1 and "never hard-code" in p1)
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

# -- the fallback: a reply with no file gets one more try --------------
tmp = Path(tempfile.mkdtemp(prefix="rigtest_"))
try:
  conf = sandbox(tmp, "| 1 | Fine. | remember |\n| 2 | NOCODE today. | guess |\n"
                      "| 3 | Fine again. | certify |\n")
  c = json.loads(conf.read_text())
  c["backends"]["mock"]["fallback"] = {"cmd": c["backends"]["mock"]["cmd"]
                                       + ["--force"]}
  conf.write_text(json.dumps(c))
  go(conf, "--treatments", "1", "--trials", "1")
  R = rows(tmp)
  check("fallback rescues a reply that had no file",
        [x["got_code"] for x in R] == ["1", "1", "1"])
  check("only the rescued call is logged as two attempts",
        [x["attempts"] for x in R] == ["1", "2", "1"])
  check("both replies are kept",
        (tmp / "runs/toy/t1/trial01/step02/reply2.txt").exists())
finally:
  shutil.rmtree(tmp, ignore_errors=True)

# -- the Ollama backend, against a fake server ------------------------
import http.server, threading
seen = []
class Fake(http.server.BaseHTTPRequestHandler):
  def do_POST(self):
    q = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
    seen.append(q)
    full = "FILLCTX" in q["prompt"]
    out = json.dumps(dict(response="```python\nprint('hi')\n```",
                          prompt_eval_count=4096 if full else 321,
                          eval_count=12)).encode()
    self.send_response(200); self.end_headers(); self.wfile.write(out)
  def log_message(self, *a): pass
srv = http.server.HTTPServer(("127.0.0.1", 0), Fake)
threading.Thread(target=srv.serve_forever, daemon=True).start()
tmp = Path(tempfile.mkdtemp(prefix="rigtest_"))
try:
  conf = sandbox(tmp, "| 1 | Fine. | remember |\n| 2 | FILLCTX. | guess |\n"
                      "| 3 | Fine again. | certify |\n")
  c = json.loads(conf.read_text())
  c["backend"] = "fake"
  c["backends"]["fake"] = dict(url=f"http://127.0.0.1:{srv.server_port}",
                               model="m", options=dict(num_ctx=4096))
  conf.write_text(json.dumps(c))
  r = go(conf, "--treatments", "1", "--trials", "2")
  R = rows(tmp)
  check("ollama backend: 6 calls, all ran", len(R) == 6 and
        all(x["ran_ok"] == "1" for x in R))
  check("token counts are logged", R[0]["prompt_tokens"] == "321" and
        R[0]["reply_tokens"] == "12")
  check("request is stateless and sets num_ctx and a seed",
        all("context" not in q and q["stream"] is False and
            q["options"]["num_ctx"] == 4096 and "seed" in q["options"]
            for q in seen))
  check("each call gets its own seed",
        len({q["options"]["seed"] for q in seen}) == 6)
  check("a prompt that fills the context is flagged",
        all("truncated" in x["error"] for x in R if x["step"] == "2") and
        all(not x["error"] for x in R if x["step"] != "2"))
finally:
  srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)

# -- prompt v3: one repair round, on training rows only ------------------
tmp = Path(tempfile.mkdtemp(prefix="rigtest_"))
try:
  conf = sandbox(tmp, "| 1 | REPAIRME first. | certify |\n"
                      "| 2 | GOODFIRST now. | certify |\n"
                      "| 3 | Fine. | remember |\n")
  c = json.loads(conf.read_text())
  c.update(repair=True, prompt_version=3)
  conf.write_text(json.dumps(c))
  r = go(conf, "--treatments", "1", "--trials", "1")
  R = rows(tmp)
  s1 = tmp / "runs/toy/t1/trial01/step01"
  check("v3: a crashing function triggers exactly one repair",
        R[0]["repaired"] == "1" and R[0]["attempts"] == "2"
        and R[0]["check_before"] == "error" and R[0]["check_after"] == "ok")
  check("v3: the repaired file replaces the first, which is kept",
        "raise ValueError" not in (s1 / "step01.py").read_text()
        and "raise ValueError" in (s1 / "first_try.py").read_text())
  rp = (s1 / "repair_prompt.txt").read_text()
  check("v3: the repair prompt shows the error and the file's own line",
        "ValueError: boom" in rp and "step01.py" in rp and "It failed:" in rp)
  check("v3: no local path reaches the repair prompt",
        str(tmp) not in rp and str(RIG) not in rp)
  check("v3: a file that passes the check is not repaired",
        R[1]["repaired"] == "0" and R[1]["check_before"] == "ok"
        and R[1]["attempts"] == "1")
  check("v3: a repair that still fails is logged as failing",
        R[2]["repaired"] == "1" and R[2]["check_after"] != "ok")
  check("v3: prompt version is logged", R[0]["prompt_version"] == "3")
  # The check must be given the training file and never the test file.
  seen_args, real = [], run.subprocess.run
  def spy(cmd, **kw):
    seen_args.extend(map(str, cmd)); return real(cmd, **kw)
  run.subprocess.run = spy
  try:
    cfg = run.load_config(str(conf))
    st, _ = run.contract_check(cfg, "toy", s1, "step01.py", "certify")
  finally:
    run.subprocess.run = real
  check("v3: the contract check reads the training file only",
        st == "ok" and any(a.endswith(".train.csv") for a in seen_args)
        and not any(a.endswith(".test.csv") for a in seen_args))
finally:
  shutil.rmtree(tmp, ignore_errors=True)

# -- the Gemini backend, against a fake server ------------------------
gseen, gcount = [], [0]
class FakeGemini(http.server.BaseHTTPRequestHandler):
  def do_POST(self):
    gcount[0] += 1
    q = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
    gseen.append(dict(path=self.path, key=self.headers.get("x-goog-api-key"), body=q))
    if gcount[0] == 1:                         # first request: rate limited
      self.send_response(429); self.end_headers(); self.wfile.write(b"{}"); return
    out = json.dumps({"candidates": [{"finishReason": "STOP", "content": {"parts": [
      {"text": "secret plan", "thought": True},
      {"text": "```python\nprint('hi')\n```"}]}}],
      "usageMetadata": {"promptTokenCount": 50, "candidatesTokenCount": 7,
                        "thoughtsTokenCount": 3}}).encode()
    self.send_response(200); self.end_headers(); self.wfile.write(out)
  def log_message(self, *a): pass
gsrv = http.server.HTTPServer(("127.0.0.1", 0), FakeGemini)
threading.Thread(target=gsrv.serve_forever, daemon=True).start()
tmp = Path(tempfile.mkdtemp(prefix="rigtest_"))
try:
  conf = sandbox(tmp, GOOD)
  (tmp / "k").write_text("TESTKEY-123")
  c = json.loads(conf.read_text())
  c["backend"] = "gem"
  c["backends"]["gem"] = dict(api="gemini", model="m-lite", backoff=0,
                              url=f"http://127.0.0.1:{gsrv.server_port}",
                              key_file=str(tmp / "k"), options={"temperature": .2})
  conf.write_text(json.dumps(c))
  go(conf, "--treatments", "1", "--trials", "1")
  R = rows(tmp)
  check("gemini backend: 3 calls, all got code and ran",
        len(R) == 3 and all(x["got_code"] == "1" and x["ran_ok"] == "1" for x in R))
  check("a 429 is retried, not logged as a failure", gcount[0] == 4)
  check("key goes in a header, never in the URL",
        all(g["key"] == "TESTKEY-123" and "TESTKEY" not in g["path"] for g in gseen))
  check("request is one user turn with a seed",
        all(len(g["body"]["contents"]) == 1 and "seed" in g["body"]["generationConfig"]
            for g in gseen))
  check("thought parts are not taken as the reply; thinking tokens are counted",
        R[0]["reply_tokens"] == "10" and R[0]["prompt_tokens"] == "50")
finally:
  gsrv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)

# -- the real requirements docs parse ---------------------------------
cfg = run.load_config()
for dom in cfg["domains"]:
  a = run.asks(cfg, dom)
  check(f"{dom}: ten asks, one per skill, in ladder order",
        [s for _, _, s in a] == run.SKILLS)

print(f"\nfailures: {fails}")
sys.exit(fails > 0)
