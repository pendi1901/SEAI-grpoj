# Shrinking code: does a good library mean less new code?

CSC 591 (SE for AI), NC State, Fall 2026. Pendyala Ritvik and Luke Shafer.

We ask an LLM to build ten data-mining skills, one step at a time, on
three MOOT data sets, and measure how much new code each step needs and
how good the result is. If a well-factored library helps, new code per
step should shrink while quality holds.

## Setup

- Data: `process/pom3a`, `hpo/Health-ClosedIssues0000` and HR attrition;
  1,000 random rows each, split 800 train / 200 test.
- Skills: remember, guess, certify, flow, blame, justify, choose, fix,
  spot, race. Customer asks are in [docs/requirements.md](docs/requirements.md).
- Treatments: plain Python (T1), scikit-learn (T3) and ezr (T5), each also
  run with an instruction to reuse earlier steps (T2, T4, T6). T7 is
  written by hand.
- Model: `gemini-3.1-flash-lite`, one fresh call per step.
- Scoring: every program runs on the same 200 test rows
  ([docs/assessment.md](docs/assessment.md)); treatments are compared with
  `same` from ezr ([docs/stats.md](docs/stats.md)).

## Results (three trials, 20 asks)

1,080 Gemini programs (3 trials x 3 domains x 6 treatments x 20 steps).
The whole run cost $4.55. T7 so far covers the process domain only.

| treatment | function worked | new lines per step | quality (Z) |
|---|--:|--:|--:|
| T1 plain | 178/180 | 57 | 0.18 |
| T2 plain + reuse | 179/180 | 50 | 0.32 |
| T3 sklearn | 177/180 | 56 | 0.53 |
| T4 sklearn + reuse | 158/180 | 49 | 0.38 |
| T5 ezr | 154/180 | 41 | -0.11 |
| T6 ezr + reuse | 153/180 | 37 | -0.11 |
| T7 by hand (process) | 20/20 | 23 | 0.77 |

ezr gives the smallest generated code but the lowest quality; most of its
losses are crashes in choose and race, where the code mishandles ezr's
rows. scikit-learn gives the best generated quality. Asking the model to
reuse earlier steps cut code for every library but did not raise quality.
T7's 23 lines per step leave out 265 lines of shared helpers, and it took
about 8 hours of human time. With three trials, `same` has little power,
so treat the ranks as provisional.

All tables and plots are in [results/report.md](results/report.md).
T7 for health and HR is in progress.

## Running it

    python rig/run.py fetch
    python rig/run.py go
    python rig/t7.py
    python rig/score.py --workers 8
    python rig/report.py

`run.py go` needs a Gemini key in `rig/.secrets/gemini_key` or
`GEMINI_API_KEY`. Tests: `python rig/test_run.py` (also `test_score.py`,
`test_report.py`, `test_t7.py`). More detail in [rig/README.md](rig/README.md).
