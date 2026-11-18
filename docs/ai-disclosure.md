# AI use: what was written by an LLM, and the errors caught

The rubric gives 3 marks for this: "what the LLM wrote, which of its
errors you caught; zero caught errors reads as zero checking". Keep it
up to date; the report's AI disclosure section is drawn from it.

Two different LLM roles appear in this project. Keep them apart:

- **The assistant** (Claude, via Claude Code) helped build the project.
- **The subject** (Gemini, earlier Ollama models) is what the experiment
  measures, in treatments 1 to 6. Its errors are results, reported in
  Results, not here.

## What the assistant wrote

| part | status |
|---|---|
| All tooling in `rig/` (runner, scorer, report, T7 registration, tests) | written by the assistant at the team's request; reviewed and tested |
| First drafts of `docs/requirements/*.md` | drafts; the team must edit them and get the lecturer's okay |
| `docs/assessment.md` | drafted by the assistant; reviewed, changed and signed off by the team on Nov 17 |
| `docs/brief.md`, `stats.md`, `domains.md`, `lecturer-notes.md`, `open-questions.md`, `talk.md`, `status.md` | drafted by the assistant from the course repo and the lecturer's posts |
| Treatment 7 (`t7/`) | **none**: must be written by hand (A21) |

## Errors in the assistant's work that were caught

Each was found by a test, by checking results, or by a team question,
and fixed before results were reported.

| # | error | how it was caught | effect if missed |
|--:|---|---|---|
| 1 | Generated programs that printed a non-ASCII character were run under the Windows console code page and logged as crashes | reading a failed program's output | working programs counted as failures |
| 2 | Rank ties on the median were broken by name, so in HR certify a treatment scoring 0.67 was ranked above one scoring 0.88 | checking the first full report | wrong rank tables |
| 3 | Race and fix programs that failed on every run were labelled "ok" | checking zero scores | success counts overstated |
| 4 | Customer asks quote full data sizes ("10,000 setups") but treatments got the 80% file; 18 demos hard-coded the count and crashed | a team question ("only 66 ran clean?") | instrument faults counted against the model |
| 5 | The prompt-v2 fix for item 4 made demos pass raw strings to their own functions, halving demo success | comparing v1 and v2 on the same calls | demos looked worse for an instrument reason |
| 6 | The contract check used a smaller row pool than the scorer, failing a working race program | checking the check against known results | the repair round would "fix" working code |
| 7 | Error messages sent back to the model contained local file paths, including the user name | review before the first repair call | personal data sent to the model provider |
| 8 | The scorer rejected numpy integers and arrays, wrongly failing 4 scikit-learn programs | code audit, Nov 18 | the scikit-learn treatments penalised for their library |
| 9 | A network or API error was logged as the model failing, and never retried | code audit, Nov 18 | an outage would look like bad scores |
| 10 | Two overlapping scoring runs wrote a duplicate row | checking a timeout listed twice | double-counted results |
| 11 | "Beat dumb baseline" compared choose and race with their failure value (0) instead of a no-effort answer (about 0.5) | code audit, Nov 18 | competency overstated |
| 12 | `t7.py --check` tested the repo's T7 folder instead of the registered steps | its test | the T7 test command would test the wrong files |
| 13 | Several patch scripts mangled `\n` escapes or duplicated a README section | syntax checks and tests | broken code or docs |

## Decisions the team made against the assistant's first suggestion

- Thinking mode on the local model: the assistant first switched it
  off; the team asked whether that hurt quality, and a test showed it
  did (1 of 6 programs worked off, 5 of 6 on).
- The local model was dropped for Gemini on the team's call, after a
  pilot showed it worked far better at low cost.
