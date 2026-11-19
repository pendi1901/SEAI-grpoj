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

## First results (one trial)

169 of 180 programs worked. The whole run cost about $0.60 and took 12 minutes.

| treatment | worked | new lines per step | quality (Z) |
|---|--:|--:|--:|
| T1 plain | 30/30 | 56 | 0.56 |
| T2 plain + reuse | 30/30 | 50 | 0.70 |
| T3 sklearn | 30/30 | 52 | 0.71 |
| T4 sklearn + reuse | 28/30 | 46 | 0.16 |
| T5 ezr | 25/30 | 40 | -0.80 |
| T6 ezr + reuse | 26/30 | 38 | -0.76 |

ezr gives the smallest code but the lowest quality. Most of its losses are
crashes in the choose and race skills, where the generated code mishandled
ezr's rows. Telling the model to reuse earlier steps cut code for plain
Python and scikit-learn. With a single trial these rankings are provisional.

All tables and plots are in [results/report.md](results/report.md).
The hand-written treatment (T7) is in progress.

## Running it

    python rig/run.py fetch
    python rig/run.py go
    python rig/t7.py
    python rig/score.py --workers 8
    python rig/report.py

`run.py go` needs a Gemini key in `rig/.secrets/gemini_key` or
`GEMINI_API_KEY`. Tests: `python rig/test_run.py` (also `test_score.py`,
`test_report.py`, `test_t7.py`). More detail in [rig/README.md](rig/README.md).
