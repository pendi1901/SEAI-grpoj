# The shrinking-code experiment

CSC 591 graduate project, SE for AI, NC State, Fall 2026.
Pendyala Ritvik and Luke Shafer.

**Question.** Does a well-factored library let an LLM build each new
skill with *less new code*, without losing quality?

- **Timm hypothesis:** with a good library (ezr), new code per step shrinks
  and quality holds.
- **Rival:** the library does not help; new code stays flat, or quality drops.

## Design

| | |
|---|---|
| Domains | three MOOT data sets: `process/pom3a` (agile process), `hpo/Health-ClosedIssues0000` (project health), HR attrition |
| Data | at most 1,000 random rows per domain (seed 1), split 80/20: 800 to build, 200 held out |
| Skills | ten per domain, one per step: remember, guess, certify, flow, blame, justify, choose, fix, spot, race |
| Requirements | twenty customer asks per domain, skill-tagged ([docs/requirements.md](docs/requirements.md)); steps use asks 1-10 |
| Treatments | T1 plain Python, T3 scikit-learn, T5 ezr; T2, T4, T6 the same plus "reuse earlier steps"; T7 by hand |
| Model | Gemini `gemini-3.1-flash-lite`, temperature 0.2, one fresh stateless call per step, one repair round on training data only |
| Scoring | every program scored on the same 200 held-out rows, per-skill Q ([docs/assessment.md](docs/assessment.md), agreed Nov 17); failures earn the baseline |
| Statistics | the lecturer's `same` (Cohen 0.35, Cliff's delta, KS); ranks per step and pooled Z ([docs/stats.md](docs/stats.md)) |

## Results so far: Gemini, N = 1 (Nov 18)

180 calls (3 domains x 6 treatments x 10 steps), **169 of 180 functions
worked**, about **$0.60** and **12 minutes** in all. Full tables:
[results/report.md](results/report.md).

| treatment | functions worked | new lines per step (median) | lines rank | quality (median Z) | quality rank | cost |
|---|--:|--:|--:|--:|--:|--:|
| T1 plain | 30/30 | 56 | 3 | 0.56 | 1 | $0.08 |
| T2 plain + reuse | 30/30 | 50 | 2 | 0.70 | **0** | $0.07 |
| T3 sklearn | 30/30 | 52 | 2 | 0.71 | **0** | $0.08 |
| T4 sklearn + reuse | 28/30 | 46 | 1 | 0.16 | 1 | $0.09 |
| T5 ezr | 25/30 | 40 | **0** | -0.80 | 2 | $0.14 |
| T6 ezr + reuse | 26/30 | 38 | **0** | -0.76 | 2 | $0.13 |

Rank 0 is best; treatments sharing a rank are indistinguishable by `same`.

**Reading.**

1. **Code shrinks with ezr.** ezr needs the fewest new lines (38-40 per step),
   and the reuse instruction cuts plain Python (56 to 50) and scikit-learn
   (52 to 46).
2. **Quality does not hold with ezr.** The ezr treatments rank last on quality.
3. **So far this favours the rival:** the code shrinks, but quality drops.

**Why ezr loses.** All 11 failures were runtime errors, none syntax:

- 8 were ezr misuse in choose and race (row indices, rows used as dict keys,
  text treated as numbers);
- 2 were scikit-learn programs given HR's `?` missing values;
- 1 broke the 50-label budget.

The course spec's next step for a losing ezr (rewire the oracle, tune ezr with ezr) is planned.

**Caveat.** N = 1; per-step ranks are provisional (see open question Q22).

## Not done yet

- **T7 (by hand):** not started. The plumbing to register, check and score it is ready ([t7/README.md](t7/README.md)).
- **N:** waiting on the lecturer's answer to how many trials (Q22).
- **Report:** the final acmart report is due Nov 30.

Every instruction is checked in [docs/status.md](docs/status.md).

## Reproduce

    python rig/run.py fetch          # MOOT data
    python rig/run.py go             # T1-T6 on Gemini (key in rig/.secrets/gemini_key or GEMINI_API_KEY)
    python rig/t7.py                 # register hand-written T7
    python rig/score.py --workers 8  # score on the held-out rows
    python rig/report.py             # results/report.md and figures

Tests: `python rig/test_run.py`, `test_score.py`, `test_report.py` and
`test_t7.py` each print `failures: 0`.

## Map

| file | what it answers |
|---|---|
| [results/report.md](results/report.md) | every table and histogram from the run |
| [docs/status.md](docs/status.md) | the project against every instruction, and what is owed |
| [docs/brief.md](docs/brief.md) | the course spec in one place |
| [docs/lecturer-notes.md](docs/lecturer-notes.md) | the lecturer's later instructions and what they changed |
| [docs/assessment.md](docs/assessment.md) | how each skill is scored (signed off Nov 17) |
| [docs/stats.md](docs/stats.md) | `same`, ranks, Q and Z |
| [docs/requirements.md](docs/requirements.md) | three clients, twenty asks each |
| [docs/domains.md](docs/domains.md) | the three data sets and their traps |
| [docs/open-questions.md](docs/open-questions.md) | questions for the lecturer |
| [docs/ai-disclosure.md](docs/ai-disclosure.md) | what the AI assistant wrote and the errors caught |
| [rig/README.md](rig/README.md) | the tooling |
| [t7/README.md](t7/README.md) | treatment 7 rules |

Course: `github.com/txt/seai26f`. Data: `github.com/timm/moot`.
