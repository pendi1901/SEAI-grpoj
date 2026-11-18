# rig: the experiment tooling

Runs treatments 1 to 6 (an LLM writes each skill), registers treatment 7
(written by hand, see `t7/README.md`), scores every program on one fixed
test suite, and reports the comparison of all seven.

Written with LLM help (Claude); disclose that in the report. None of it
is treatment 7, and none of it counts in any treatment's line totals.

## The pipeline

From the repo root. One config, `rig/config.json`; no flags needed.

    python rig/run.py fetch            # data sets + ezr.py, once
    python rig/run.py plan             # what would run: 180 calls per trial
    python rig/run.py go               # T1-T6, N = 1 (about $0.50, under an hour)
    python rig/run.py status           # progress and ETA
    python rig/t7.py                   # register the hand-written T7 files
    python rig/score.py --workers 8    # grade every program
    python rig/report.py               # results/report.md and results/fig/

`go` resumes: a finished call is never repeated, and `--trials 3` later
adds trials 2 and 3 to the same folders. Narrow with `--domains hr` or
`--treatments 5 6`; time-test with `--limit 10`.

Tests, no model and no network: `python rig/test_run.py`,
`test_score.py`, `test_report.py`, `test_t7.py` (each wants "failures: 0").

## Files

| file | job |
|---|---|
| `config.json` | the one config: model, prompt version, data cap, treatments, domains, levers, prices |
| `run.py` | builds each prompt, calls the model, saves every file, logs every call |
| `contract.py` | the function each skill must define, its rules, failure and no-effort values |
| `score.py` | grades programs on the test suite; `--check` runs one on training rows |
| `report.py` | rank tables with `same`, Z, histograms, competency and cost |
| `t7.py` | registers and demos the hand-written treatment 7 |
| `mock_llm.py` | a fake model for the tests |
| `lib/ezr.py` | the lecturer's Python ezr (`timm/ezr`), given to T5 and T6 |
| `.secrets/` | the Gemini API key; git-ignored, never committed |

## Settings, and what Methods must state

| setting | value | why |
|---|---|---|
| model | `gemini-3.1-flash-lite`, temperature 0.2, a seed per call | cheapest Gemini model the key can use; competent where a local 9B model was not (`docs/archive/`) |
| data | 1,000 random rows per domain, split 800 / 200 with seed 1 | lecturer's A23; one test suite for every treatment (Nov 16 notes) |
| steps | ten per domain, asks 1-10, one per skill | A21: "all ten skills" |
| reset | one stateless API call per step, in a fresh folder; no history, no CLAUDE.md | uproj.md reset rule |
| no-reuse treatments | still see the earlier steps' code, but are not told to reuse it | uproj.md: supply "the code for skills 1..i" in every treatment (open question 6) |
| prompt version | 3 | below |

### Prompt version 3: clearer contract, one repair round

**Clearer contract.** Each prompt shows the header and two rows exactly
as the function receives them, every text column with its values, and
each skill's rules with what breaking them costs (`RULES` in
`contract.py`). These restate the signed-off `docs/assessment.md`; they
describe the data and the harness, never how to solve a skill.

**One repair round.** When a file comes back, its function is called on
a sample of the *training* data under the scorer's own rules, sizes and
label budget (fewer repetitions only). If that fails, the model gets one
more call: the original prompt, its file and the error. The corrected
file replaces the first (kept as `first_try.py`). There is no second
repair. In Methods: "an LLM with one repair round on training data".
T7 also runs its own code before submitting, so this brings the LLM
treatments closer to it.

- The check never reads the test file (a test confirms it).
- The error shown keeps only the generated file's frames and library
  frames, each cut to a bare file name: no local path or user name is
  sent to the model provider.
- Logged per call: `check_before`, `check_after`, `repaired`, and the
  extra call in `attempts`, `llm_secs` and the token counts.

### Earlier prompt versions

| version | run | where |
|---|---|---|
| 1 | Ollama `ornith:9b`, N = 1 | tag `archive/first-runs`, `runs/` and `results/` |
| 2 | adds the file's true row count; Gemini N = 1, and a stopped Ollama run | same tag, `runs-gemini/`, `results-gemini/`, `runs-v2/` |
| 3 | current | `runs/`, `results/` |

Never pool results across prompt versions or models.

## When the model cannot be reached

Rate limits, server errors, dropped connections and timeouts are retried
with back-off. If a call still fails, nothing is logged and its folder is
removed: the step is not counted as the model failing, and the next
`go` makes it again. A missing file, a crash or a broken rule *is* a
result and is logged.

## The scorer

How each skill is judged is defined in `docs/assessment.md` (signed off
by the team) and summarised in `docs/stats.md`. Mechanics:

- Every program for one skill in one domain faces the same test cases,
  seeded by domain and skill, built from the held-out 200 rows.
- Each test case gives one number; Q is their mean. A missing function,
  a crash, a timeout (300 s) or a broken rule earns the failure value
  on every case. `status` says which: `ok`, `invalid`, `error`,
  `timeout`, `no_code`.
- Any whole number counts as a row position, numpy's included.
- Only one `score.py` may run on a results folder at a time
  (`scoring.lock`); a second is refused.

Outputs beside `results/calls.csv`: `scores.csv` (one row per program)
and `cases.jsonl` (the per-test-case numbers that `same` compares).

## The report

`results/report.md`, per domain and for all domains together:

- **Competency and cost** per treatment: programs, demos that ran,
  functions that worked, programs that beat a no-effort answer, new
  LOC, tokens, dollars, clock minutes (lecturer's A23 and A28).
- **Per skill on the test suite**: each treatment's mean and its `same`
  rank. Rank 0 is the best group; a shared rank means `same` could not
  tell them apart. `same` is the lecturer's Python one with all three
  tests (Cliff's delta, Kolmogorov-Smirnov, Cohen at 0.35). Ties on the
  median are broken by the mean.
- New lines and Q per step, Z rescaled within each domain and skill,
  and the "% new code" histogram (one line per treatment, T7 in black).

A known limit, stated in the archived write-ups: "% new code" is new
lines over all lines so far, so it falls for every treatment; reuse
shows in absolute new lines, not in that histogram's slope.
