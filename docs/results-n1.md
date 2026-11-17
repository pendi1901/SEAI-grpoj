# First full run: N = 1, three domains, six LLM treatments

Run Nov 17 2026 on local Ollama, `ornith:9b`, thinking on, one retry
with thinking off when no file came back. Code at commit `e797df6`
(`results/run-commit.txt`). 180 LLM calls, about 96 s each, 4.8 hours
in all. Scored on the held-out 20% of each data set under the rules
the team signed off in [assessment.md](assessment.md). Full tables:
`results/report.md`; figures: `results/fig/`. Treatment 7 (hand-written)
is not done yet, so nothing here compares the LLM with a human.

## What can be claimed

Only differences that `same` certifies. With N = 1, per-step cells hold
one number each, so per-step ranks are orderings, not statistics. The
pooled tables (30 values per treatment) and the per-skill test-suite
tables (14 to 400 test cases per cell) are where `same` has data.

1. **The ezr library cut new code; the reuse instruction did not.**
   Median new lines per step, pooled over all domains and steps:
   T5 ezr 34 and T6 ezr+reuse 38 share rank 0; the other four (51 to 61)
   share rank 1. Within each library, reuse and no-reuse share a rank.
2. **The reuse instruction changed behaviour, not size.** Files at
   steps 2 to 10 that import an earlier step: T2 22%, T4 69%, T6 44%;
   T1, T3, T5 0%. Importing earlier steps did not shrink the new file.
3. **No treatment is better on quality overall.** On Q rescaled to Z
   within each domain and skill and pooled, all six share rank 0.
4. **Most programs failed.** 81 of 180 were scored without error
   (45%). 88 crashed, 9 broke the rules, 2 returned no file. Failures
   earn the skill's baseline, so they pull every treatment toward the
   same score; this is the main reason item 3 shows no difference.

## What this says about the hypotheses

Neither side wins cleanly, and the reason is mostly the instrument.

- **The course's histogram cannot decide it here.** "% new code per
  step" is new lines divided by all lines written so far, so it falls
  for every treatment as the denominator grows. In all three domains
  the six lines fall together from 100% to about 15%, reuse or not
  (`results/fig/*.png`). Falling bars are not evidence of reuse unless
  the reuse lines fall faster, and they do not.
- **New lines per step rose, not fell.** Median new lines, steps 1 to
  3 against steps 8 to 10: T1 40 to 72, T2 57 to 81, T3 37 to 78, T4 42
  to 82, T5 28 to 67, T6 34 to 66. The later skills (fix, spot, race)
  are larger tasks, so skill order and reuse are confounded.
- **Read narrowly, the evidence leans to the rival** for the reuse
  instruction (no size effect) and to the Timm hypothesis for the
  library (ezr, a factored library, needed less new code). That split
  is itself a finding worth stating.

## Skills that cannot separate treatments in this run

| skill | what happened | why |
|---|---|---|
| race | every program scored 0 | all crashed or used more than 50 labels |
| choose | about 0 everywhere | 14 of 18 crashed; the rest lost to random |
| guess | 0 in HR and health | 13 of 18 crashed, mostly on hidden `?` cells |
| remember | the same 0.69 or 0.73 for most treatments | it sees the goals, so sorting by them is a full answer (assessment doubt 5) |
| spot | 0.50, the maximum, for four treatments in process | planted errors 6 standard deviations out are too easy (doubt 4) |

## Problems found in the tooling while checking, and fixed

Both were found by reading the results, fixed, tested, and the 180
programs rescored. No LLM call was repeated and no Q value changed.

- **Rank order on 0/1 data was wrong.** Skills such as certify give
  0/1 test cases, so most treatments shared a median and the tie was
  broken by name. In HR certify, T1 (0.67) was ranked ahead of T2
  (0.88). Ties on the median are now broken by the mean.
- **"ok" overstated success for race and fix.** Those scorers catch
  failures run by run, so a program that failed on every run was
  labelled "ok" with Q = 0. It is now labelled an error. The report's
  "scored without error" counts fell from 105 to 81.

## Errors in the LLM's code worth citing in the AI disclosure

- Converting hidden `?` goal cells to numbers (11 programs), though
  the prompt says hidden cells are `?`.
- Treating rows as dicts and indexing them by column name (about 10).
- A flow program that keeps scores in a module-level list that never
  resets, so its threshold drifts across the scorer's 100 orders.
- A flow script that replays all 16,000 training rows with a
  quadratic loop and timed out.
- Race programs that spent more than 50 labels, or did not name a
  strategy "random".

## Caveats

N = 1; one model, a 9B local one; one 80/20 split; the scorer's
reading of gloss10 is ours. Whether per-test-case numbers can stand
in for N >= 10 repeats is open question Q22.

## Suggested next steps

1. **Treatment 7.** The lecturer asked for it before more automatic
   runs, and it is the only comparison against a human.
2. **A paired comparison.** Compare reuse against no-reuse at the same
   step, so skill difficulty cancels out, instead of reading the
   falling histogram.
3. **Ask the lecturer** about the histogram artefact and about Q22,
   with these numbers in hand.
4. More repeats only after that: at about 5 hours per repeat, N = 3
   is a 10-hour addition.
