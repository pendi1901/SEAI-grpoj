#!/usr/bin/env python3
"""
report.py: turn the two logs into the tables and figures of Results.

  python rig/report.py            # writes results/report.md and results/fig/

Reads results/calls.csv (one row per LLM call) and results/scores.csv
(one Q per program). Works on a partial run. Produces, per domain:

  1. the histogram: % new code per step, one line per treatment;
  2. `same` tables: treatments ranked on new lines and on Q, step by step;
  3. Q re-expressed as Z within each (domain, skill), so that treatments
     can be compared across skills and domains.

Statistics: `same` is the lecturer's Python version (rig/lib/ezr.py) with
eps=0.35, which makes it the three-test rule of gloss6: Cohen, Cliff's
delta and Kolmogorov-Smirnov must all agree. `ranks` is ported from the
course's ezr.lua.

Written with LLM help; experiment tooling, not part of treatment 7.
"""
import argparse, csv, statistics as st, sys
from collections import defaultdict
from pathlib import Path

RIG = Path(__file__).resolve().parent
sys.path.insert(0, str(RIG))
sys.path.insert(0, str(RIG / "lib"))
import run

EPS = 0.35
NAMES = {"1": "T1 plain", "2": "T2 plain+reuse", "3": "T3 sklearn",
         "4": "T4 sklearn+reuse", "5": "T5 ezr", "6": "T6 ezr+reuse",
         "7": "T7 human"}


def same(xs, ys):
  "Indistinguishable under Cliff's delta, KS and Cohen (all three)."
  import ezr
  if len(set(xs)) == 1 and xs == ys: return True       # no spread at all
  return ezr.same(xs, ys, eps=EPS)


def ranks(d, big=False):
  """Port of ezr.lua's ranks. D maps a name to a list of numbers. Sort by
  median, best first; a treatment gets a new rank only when it is not
  `same` as the leader of the current rank. So ties share a rank.

  One departure: equal medians are broken by the mean, not by name. Many
  skills give 0/1 test cases (certify, choose, race, fix), where most
  treatments share a median; sorting those by name made a worse
  treatment the rank-0 leader. The median rule is unchanged otherwise."""
  med = lambda v: sorted(v)[len(v) // 2]
  sign = -1 if big else 1
  out, rank, best = {}, -1, None
  for k in sorted(d, key=lambda k: (sign * med(d[k]),
                                    sign * st.mean(d[k]), k)):
    if best is None or not same(d[best], d[k]):
      rank, best = rank + 1, k
    out[k] = rank
  return out


def load(cfg):
  "Calls joined to their scores: a list of dicts with numbers as numbers."
  calls = list(csv.DictReader(open(cfg["log"], encoding="utf8")))
  sp = cfg["log"].with_name("scores.csv")
  score = ({r["dir"]: r for r in csv.DictReader(open(sp, encoding="utf8"))}
           if sp.exists() else {})
  for c in calls:
    for k in ("step", "trial", "new_lines", "total_lines"): c[k] = int(c[k])
    c["pct_new"] = float(c["pct_new"])
    if str(c["got_code"]) != "1": c["new_lines"] = None    # no file: missing
    s = score.get(c["dir"])
    c["q"] = float(s["q"]) if s else None
    c["status"] = s["status"] if s else "unscored"
    c["cases"], c["extra"] = None, {}
  cp = cfg["log"].with_name("cases.jsonl")
  if cp.exists():
    import json
    by = {}
    for line in open(cp, encoding="utf8"):
      if line.strip():
        j = json.loads(line); by[j["dir"]] = j
    for c in calls:
      j = by.get(c["dir"]) or {}
      c["cases"], c["extra"] = j.get("cases"), j.get("extra") or {}
  return calls


def add_z(calls):
  "Z = (Q - mean) / sd over every scored call of that domain and skill."
  pool = defaultdict(list)
  for c in calls:
    if c["q"] is not None: pool[c["domain"], c["skill"]].append(c["q"])
  for c in calls:
    v = pool.get((c["domain"], c["skill"]), [])
    sd = st.pstdev(v) if len(v) > 1 else 0
    c["z"] = (None if c["q"] is None else
              0.0 if sd == 0 else (c["q"] - st.mean(v)) / sd)


def table(head, rows):
  out = ["| " + " | ".join(head) + " |",
         "|" + "|".join("---" if j == 0 else "--:" for j in range(len(head)))
         + "|"]
  return "\n".join(out + ["| " + " | ".join(str(x) for x in r) + " |"
                          for r in rows])


def rank_table(calls, key, big, fmt):
  """One row per treatment, one column per step: median of KEY across
  trials, with its rank in brackets. Rank 0 is the set of winners."""
  steps = sorted({c["step"] for c in calls})
  treats = sorted({c["treatment"] for c in calls})
  cell = defaultdict(dict)
  for s in steps:
    d = defaultdict(list)
    for c in calls:
      if c["step"] == s and c[key] is not None: d[c["treatment"]].append(c[key])
    if not d: continue
    r = ranks(d, big) if len(d) > 1 else {k: 0 for k in d}
    for t in d:
      cell[t][s] = f"{fmt(sorted(d[t])[len(d[t]) // 2])} ({r[t]})"
  return table(["treatment"] + [f"s{s}" for s in steps],
               [[NAMES.get(t, t)] + [cell[t].get(s, "") for s in steps]
                for t in treats])


def case_table(calls):
  """The comparison the lecturer asked for: per skill, each treatment's
  list of per-test-case numbers (pooled over its trials), compared with
  `same`. Cell = mean (rank). Every treatment faced the same test cases."""
  treats = sorted({c["treatment"] for c in calls})
  rows = []
  for skill in run.SKILLS:
    d = defaultdict(list)
    for c in calls:
      if c["skill"] == skill and c["cases"]: d[c["treatment"]] += c["cases"]
    if not d: continue
    r = ranks(d, big=True) if len(d) > 1 else {k: 0 for k in d}
    n = max(len(v) for v in d.values())
    rows.append([skill, n] + [f"{st.mean(d[t]):.2f} ({r[t]})" if t in d else ""
                              for t in treats])
    for name in sorted({k for c in calls if c["skill"] == skill
                        for k in c["extra"]}):       # e.g. fix_helps
      d = defaultdict(list)
      for c in calls:
        if c["skill"] == skill: d[c["treatment"]] += c["extra"].get(name, [])
      r = ranks(d, big=True) if len(d) > 1 else {k: 0 for k in d}
      rows.append([name.replace("_", ": "), max(len(v) for v in d.values())]
                  + [f"{st.mean(d[t]):.2f} ({r[t]})" if d.get(t) else ""
                     for t in treats])
  return table(["skill", "cases"] + [NAMES.get(t, t) for t in treats], rows)


def overall(calls, key, big, fmt):
  "Treatments ranked on KEY pooled over every step."
  d = defaultdict(list)
  for c in calls:
    if c[key] is not None: d[c["treatment"]].append(c[key])
  if not d: return "(nothing scored yet)"
  r = ranks(d, big) if len(d) > 1 else {k: 0 for k in d}
  rows = [[NAMES.get(t, t), len(v), fmt(st.median(v)),
           fmt(st.pstdev(v) if len(v) > 1 else 0), r[t]]
          for t, v in sorted(d.items(), key=lambda kv: (r[kv[0]], kv[0]))]
  return table(["treatment", "n", "median", "sd", "rank"], rows)


def figure(calls, domain, path):
  "The histogram of the spec: x = step, y = % new code, a line per treatment."
  import matplotlib
  matplotlib.use("Agg")
  import matplotlib.pyplot as plt
  fig, ax = plt.subplots(figsize=(6.4, 3.6))
  for t in sorted({c["treatment"] for c in calls}):
    by = defaultdict(list)
    for c in calls:
      if c["treatment"] == t and c["new_lines"]: by[c["step"]].append(c["pct_new"])
    xs = sorted(by)
    style = (dict(color="black", lw=2, marker="s", ms=4) if t == "7" else
             dict(marker="o", ms=3, ls="-" if run_reuse(calls, t) else "--"))
    ax.plot(xs, [st.median(by[x]) for x in xs], label=NAMES.get(t, t),
            **style)
  ax.set(xlabel="step", ylabel="% new code (median over trials)",
         title=domain, ylim=(0, 105))
  ax.legend(fontsize=7, ncol=2)
  fig.tight_layout()
  path.parent.mkdir(parents=True, exist_ok=True)
  fig.savefig(path, dpi=150)
  plt.close(fig)


def run_reuse(calls, t):
  return any(c["reuse"] == "1" for c in calls if c["treatment"] == t)


def transfer_table(calls):
  """591 transfer evidence for T7: lines written per domain against lines
  in t7/shared, which every domain may reuse. Empty when there is no T7."""
  t7 = [c for c in calls if c["treatment"] == "7"]
  if not t7: return ""
  shared = sorted((run.ROOT / "t7" / "shared").glob("*.py"))
  lines = sum(run.code_lines(p.read_text("utf8")) for p in shared)
  rows = []
  for dom in sorted({c["domain"] for c in t7}):
    cs = [c for c in t7 if c["domain"] == dom]
    own = sum(c["new_lines"] or 0 for c in cs)
    rows.append([dom, len(cs), own, lines,
                 f"{100 * lines // max(own + lines, 1)}%"])
  return ("Treatment 7 across domains. Shared code (`t7/shared/`, "
          f"{len(shared)} files) is available to every domain; a falling "
          "per-domain count, in the order the domains were built, is the "
          "transfer the hypothesis predicts.\n\n"
          + table(["domain", "steps", "lines written for it",
                   "shared lines", "shared share"], rows))


def cost_table(calls, cfg):
  """The lecturer's talk numbers (A28) and competency numbers (A23), one
  row per treatment: did the code work, and what did it cost?"""
  from contract import DUMB
  rows = []
  for t in sorted({c["treatment"] for c in calls}):
    cs = [c for c in calls if c["treatment"] == t]
    n = len(cs)
    worked = sum(c["status"] == "ok" for c in cs)
    beat = sum(c["q"] is not None and c["q"] > DUMB[c["skill"]] + 1e-9
               for c in cs)
    tin = sum(int(c.get("prompt_tokens") or 0) for c in cs)
    tout = sum(int(c.get("reply_tokens") or 0) for c in cs)
    usd = 0.0
    for c in cs:
      b = cfg["backends"].get(c.get("backend", ""), {})
      usd += (int(c.get("prompt_tokens") or 0) * b.get("price_in_per_m", 0)
              + int(c.get("reply_tokens") or 0) * b.get("price_out_per_m", 0)
              ) / 1e6
    if t == "7":
      hm = [float(c["human_minutes"]) for c in cs if c.get("human_minutes")]
      clock = f"{sum(hm):.0f} (human)" if hm else "not logged"
    else:
      clock = f"{sum(float(c.get('llm_secs') or 0) + float(c.get('run_secs') or 0) for c in cs) / 60:.0f}"
    loc = sum(c["new_lines"] or 0 for c in cs)
    rows.append([NAMES.get(t, t), n, f"{sum(c.get('ran_ok') == '1' for c in cs)}",
                 f"{worked} ({100 * worked // max(n, 1)}%)",
                 f"{beat} ({100 * beat // max(n, 1)}%)", loc,
                 f"{tin / 1e6:.2f}M" if tin else "0",
                 f"{tout / 1e6:.2f}M" if tout else "0",
                 f"${usd:.2f}", clock])
  return table(["treatment", "programs", "demo ran", "function worked",
                "beat dumb baseline", "new LOC", "tokens in", "tokens out",
                "cost", "clock (min)"], rows)


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
  ap.add_argument("--config")
  a = ap.parse_args()
  cfg = run.load_config(a.config)
  if not cfg["log"].exists(): sys.exit(f"no {cfg['log']}")
  calls = load(cfg)
  add_z(calls)
  out_dir = cfg["log"].parent
  f1 = lambda v: f"{v:.0f}"
  f2 = lambda v: f"{v:.2f}"
  n = max(c["trial"] for c in calls)
  scored = sum(c["q"] is not None for c in calls)
  md = ["# Results", "",
        f"{len(calls)} calls logged, {scored} scored, up to {n} trials. "
        "Generated by `rig/report.py`; do not edit by hand.", "",
        "In every table a number in brackets is a rank. Rank 0 is the best "
        "group. Treatments that share a rank are not distinguishable: "
        f"`same` (Cliff's delta, Kolmogorov-Smirnov, Cohen at {EPS}) could "
        "not tell them apart.", ""]
  if n < 10:
    md += [f"**N = {n}.** With so few trials per cell `same` has little "
           "to work with: at N = 3 the Kolmogorov-Smirnov test can never "
           "report a difference. Read per-step ranks as provisional.", ""]
  for dom in sorted({c["domain"] for c in calls}):
    cs = [c for c in calls if c["domain"] == dom]
    figure(cs, dom, out_dir / "fig" / f"{dom}.png")
    wrote = sum(c["got_code"] == "1" for c in cs)
    md += [f"## {dom}", "",
           f"{len(cs)} calls; {wrote} returned a file; "
           f"{sum(c['status'] == 'ok' for c in cs)} were scored without "
           "error (the rest earn the failure value).", "",
           f"![% new code per step](fig/{dom}.png)", "",
           "### Competency and cost", "",
           "Competency (lecturer's A23): if a treatment's functions mostly "
           "fail, its other numbers say little. 'Beat dumb baseline' counts "
           "programs whose Q is above what a no-effort answer earns.", "",
           cost_table(cs, cfg), "",
           "### New lines of code per step (lower is better)", "",
           "Median over the trials that returned a file; a blank cell "
           "means none did. Few lines is only reuse if Q held up: check "
           "the next table.", "",
           rank_table(cs, "new_lines", False, f1), "",
           "### Per skill, on the test suite (higher is better)", "",
           "Mean over test cases, pooled over trials, with rank. Every "
           "treatment faced the same test cases, built from the held-out "
           "20% of the data. A failed program earns the skill's baseline "
           "on every case. This is the table to quote.", "",
           case_table(cs), "",
           "### Q per step (higher is better)", "",
           "Each step is a different skill with its own scale, so compare "
           "down a column, not along a row.", "",
           rank_table(cs, "q", True, f2), "",
           "### Over all steps", "", "New lines:", "",
           overall(cs, "new_lines", False, f1), "",
           "Z (Q rescaled within each skill; higher is better):", "",
           overall(cs, "z", True, f2), ""]
  md += ["## All domains together", "",
         "### Competency and cost", "", cost_table(calls, cfg), "",
         "### Transfer across domains (T7)", "",
         transfer_table(calls) or "No treatment-7 files registered yet.", "",
         "Z is computed within each (domain, skill), then pooled.", "",
         overall(calls, "z", True, f2), "", "New lines, pooled:", "",
         overall(calls, "new_lines", False, f1), ""]
  (out_dir / "report.md").write_text("\n".join(md), "utf8")
  print(f"wrote {out_dir / 'report.md'} and {out_dir / 'fig'}")


if __name__ == "__main__":
  main()
