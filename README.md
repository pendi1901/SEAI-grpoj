# seai26f-gproj

Notes for the CSC 591 graduate project (SE for AI, NC State, Fall
2026): the shrinking-code experiment on three MOOT domains, namely
software process (pom3a), open-source project health, and HR employee
attrition.

This repo holds the reading of the course spec, draft requirements,
and the runner for treatments 1 to 6. No experiment has been run yet.
It is local, with no remote.

| file | what it answers |
|---|---|
| [docs/plan.md](docs/plan.md) | **start here**: what to do, who does it, compute and time estimates, day by day |
| [docs/brief.md](docs/brief.md) | the whole spec: dates, marks, hypotheses, skills, treatments, report, rubric, every way to lose marks |
| [docs/stats.md](docs/stats.md) | `same`, `ranks`, the per-skill Q score, Z, and what to log after every run |
| [docs/runs.md](docs/runs.md) | how many LLM calls, how long, the reset protocol |
| [docs/domains.md](docs/domains.md) | the three data sets, measured, with their traps |
| [docs/requirements.md](docs/requirements.md) | DRAFT: three clients, twenty skill-tagged asks each |
| [rig/README.md](rig/README.md) | the runner: one command per stage, what it logs, what it does not do |
| [docs/open-questions.md](docs/open-questions.md) | what the spec leaves unsettled, and what to ask the lecturer |

Source: `github.com/txt/seai26f` at commit `5fb51c8` (Nov 16 2026) and
`github.com/timm/moot` (master, same day).

## The short version

- 39 project marks plus a 15-mark talk. Final report due Mon Nov 30.
- Three domains, one shared codebase, twenty skill-tagged customer asks
  per domain, written before coding and okayed by the lecturer.
- Seven treatments: an LLM on plain Python, scikit-learn and ezr, each
  with and without being told to reuse; the seventh is us, by hand.
- N trials, each a fresh headless LLM call in a fresh directory. N of
  10 or more for full Results marks; 3 is the floor.
- Every claimed difference certified by `same`. No `same`, no marks.
- Negative results score. Hidden ones do not.
