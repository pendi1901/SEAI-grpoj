# seai26f-gproj

CSC 591 graduate project (SE for AI, NC State, Fall 2026): the
shrinking-code experiment on three MOOT domains, namely agile software
process (pom3a), open-source project health, and staff retention (HR).

Does a well-factored library let an LLM, or a person, build each new
skill with less new code? Seven treatments build ten skills per domain:
an LLM on plain Python, scikit-learn or ezr, each with and without being
told to reuse earlier steps (T1-T6), and the team by hand (T7). Every
program is scored on one held-out test suite and the seven are compared
with the lecturer's `same` test.

**Start here: [docs/status.md](docs/status.md)**, which says what is done,
how it meets each instruction, and what is still owed.

| file | what it answers |
|---|---|
| [docs/status.md](docs/status.md) | where the project stands against every instruction |
| [docs/talk.md](docs/talk.md) | next week's 10-minute talk: slides and checklist |
| [docs/brief.md](docs/brief.md) | the course spec in one place: marks, hypotheses, treatments, rubric |
| [docs/lecturer-notes.md](docs/lecturer-notes.md) | every later instruction from the lecturer, and what it changed |
| [docs/assessment.md](docs/assessment.md) | how each skill is scored (signed off Nov 17) |
| [docs/stats.md](docs/stats.md) | `same`, ranks, Q and Z |
| [docs/requirements.md](docs/requirements.md) | three clients, twenty skill-tagged asks each (drafts) |
| [docs/domains.md](docs/domains.md) | the three data sets and their traps |
| [docs/open-questions.md](docs/open-questions.md) | what to ask the lecturer, and what only the team knows |
| [rig/README.md](rig/README.md) | the tooling: one command per stage |
| [t7/README.md](t7/README.md) | treatment 7: what to write by hand and how it is scored |
| [docs/archive/](docs/archive/README.md) | the first plan (Nov 16) |

Course source: `github.com/txt/seai26f`; data: `github.com/timm/moot`.

## Run it

    python rig/run.py fetch
    python rig/run.py go
    python rig/t7.py
    python rig/score.py --workers 8
    python rig/report.py

The Gemini key goes in `rig/.secrets/gemini_key` (git-ignored) or the
`GEMINI_API_KEY` environment variable.
`results/` and `runs/` hold the Gemini N = 1 run (prompt v3, Nov 18).
