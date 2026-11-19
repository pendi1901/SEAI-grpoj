# Status, Nov 18 2026

**Talk: Monday Nov 23** (10 minutes, at most 10 slides, mandatory).
**Final report: Monday Nov 30** (34 marks).

## Where we stand

The tooling is complete and tested: it runs treatments 1 to 6 on Gemini,
registers the hand-written treatment 7, scores every program on one
held-out test suite, and reports competency, cost and the `same`
comparison of all seven. **The Gemini N = 1 run (prompt v3, Nov 18) is
in `results/` and `runs/`**: 169 of 180 functions worked, about $0.60,
about 12 minutes. Earlier runs were deleted. **Treatment 7 has not been
started.**

## What is in the repo

| part | contents |
|---|---|
| `docs/` | the spec digest, lecturer notes, assessment sheet, stats, requirements drafts, open questions, talk plan, AI-use log, this file |
| `rig/` | runner, scorer, report, T7 registration, one config, tests (4 suites, all passing) |
| `t7/` | instructions and the exact contract for the hand-written skills; no code yet |
| `docs/archive/` | the first plan (Nov 16) |

## Every instruction, checked

Done: the repo meets it. Partly: built but waiting on something.
Not yet: still owed. Unknown: only the team knows.

### Course spec (`uproj.md`, `gproj.md`)

| instruction | status | where |
|---|---|---|
| Both hypotheses verbatim, with win conditions, first | partly: quoted, but no dated team claim in the repo | `docs/brief.md` s.3; see owed #5 |
| Claim pre-registered before coding | unknown | owed #5 |
| Three domains, three clients, three MOOT data sets | done | `docs/requirements/` |
| Twenty asks per domain, customer words, skill-tagged, at `docs/requirements.md` | done (drafts) | `docs/requirements.md` |
| Asks okayed by the lecturer | unknown | owed #5 |
| Seven treatments (3 libraries x reuse or not, plus by hand) | partly: T1-T6 built; T7 slot ready, no code | `rig/config.json`, `t7/` |
| Each LLM step given the library, the code for steps 1..i, and the one-line ask | done | `rig/run.py` |
| Reset: fresh one-shot calls, fresh folder, no memory, no CLAUDE.md | done | `rig/run.py` |
| N repeats; N >= 10 for full Results marks, 3 is the floor | not yet: planned N = 1 | open question Q22 |
| Steps git-tagged; step i+1 reuses step i | not yet for T7 | `t7/README.md` says how |
| `same` on every comparison | done | `rig/report.py` |
| Histograms of % new code per step, one line per treatment | done (from stored files; T7 from tags) | `rig/report.py` |
| 591: one shared codebase, transfer evidence across domains | partly: transfer table built; needs T7 shared code | `t7/shared/`, report |
| Fix ezr if it loses (oracle rewire, self-tuning) | not yet; only needed if ezr loses | decide after the run |
| Repo public, tests, one-command demos | partly: tests and demo command done; repo is local only | owed #8 |
| Report: `acmart`, 6-9 pages, five headers, repo URL on page one | not yet | owed #9 |
| AI disclosure: what the LLM wrote, errors caught | partly: log started | `docs/ai-disclosure.md` |

### The lecturer's later instructions

| instruction | source | status | where |
|---|---|---|---|
| Agree how each task is assessed before big runs | Nov 16 notes | done: signed off Nov 17 | `docs/assessment.md` |
| 80/20 split; the same test suite for every treatment | Nov 16 notes | done | `rig/run.py` `split`, `rig/score.py` |
| Compare the treatments with his stats | Nov 16, A28 | done | report: per-skill table |
| Do T7 first | Nov 16 notes | not yet | owed #2 |
| Python ezr is fine | Nov 16 notes | done | `rig/lib/ezr.py` |
| Budget about $100 a person; cheaper models | Nov 16 notes | done: about $0.50 spent | `rig/config.json` |
| T7: one hand-written run; LLM as search tool only | A21 | rules recorded | `t7/README.md` |
| T7 is 20-50 lines of glue to EZR or a library | A28 | not yet | owed #2 |
| At most 1,000 random rows per data set | A23 | done | `max_rows` in the config |
| Runs must take minutes, not days (6 + 2R reruns) | A23 | done by design: one pass estimated under an hour | not yet measured on v3 |
| Competency numbers from every run | A23 | done | report: competency and cost |
| Talk: LOC, tokens, $, clock time over the 7 treatments | A28 | done | same table |
| Talk: stats comparing the 7 ways | A28 | done | report: per-skill table |
| Talk mandatory, 10 minutes, at most 10 slides | Q25 | planned | `docs/talk.md` |
| Acknowledge the talk post on Discord | Q25 | unknown | owed #1 |

## Still owed

### Before Monday's talk, in this order

| # | what | who | time |
|--:|---|---|---|
| 1 | Click the Discord acknowledgement; **book a lecturer appointment and discuss the talk** (2 marks, all or nothing). Take `docs/open-questions.md` | anyone | 15 min |
| 2 | **Write treatment 7 by hand**, at least one domain, ten steps: commit and tag each step, run `python rig/t7.py --check` | team | the biggest job |
| 3 | Run the experiment: `python rig/run.py go`, then `t7.py`, `score.py`, `report.py` | anyone | under an hour, about $0.50 |
| 4 | Build at most 10 slides from `results/report.md` (outline in `docs/talk.md`); Google Slides, public, editable by timm@ieee.org; rehearse once with a timer | team | 2-3 hours |

### Before the report on Nov 30

| # | what |
|--:|---|
| 5 | Confirm the requirements are okayed and the claim is pre-registered; if the claim was never written, write it now and date it honestly |
| 6 | T7 for all three domains, with reusable code in `t7/shared/` (the transfer evidence) |
| 7 | Decide N with the lecturer's answer to Q22; extra trials resume from the first |
| 8 | Push the repo to a public GitHub repository (the report needs its URL); never commit `rig/.secrets/` |
| 9 | Write the report: `acmart`, 6-9 pages, the five headers, the AI disclosure from `docs/ai-disclosure.md` |
| 10 | Rotate both Gemini keys once the runs are done (they were pasted into a chat) |

## Risks

- **T7 is the critical path.** Without it the talk shows six of seven
  treatments and the report has no human control or transfer evidence.
- **N = 1 may cost Results marks** unless the lecturer accepts
  per-test-case numbers (Q22).
- **Prompt v3 is untested on a real model.** Run it early enough to fix
  surprises before Monday.
