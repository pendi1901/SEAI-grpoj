# Choosing the local model: trials of Nov 16 2026

Six real calls per configuration, on the HR data: treatment 1 (plain
Python, no reuse) steps 1-3, then treatment 6 (ezr, reuse) steps 1-3.
Ollama 0.32.6 in Docker with the RTX 5060 (8 GB), 16,384-token window.
These are scouting runs, kept in `timing/` (not committed) and never
to be mixed into the experiment's data.

| model | settings | done | wrote a file | ran clean | secs per call |
|---|---|--:|--:|--:|--:|
| qwen3.5:9b | thinking off, defaults (temperature 1, presence penalty 1.5), 4,096 output cap | 6 | 4 | 0 | 138 |
| qwen3.5:9b | thinking on, 8,192 output cap | 4 (stopped) | 1 | 0 | 277 |
| ornith:9b | thinking off, temperature 0.2, 8,192 output cap | 6 | 6 | 1* | 43 |
| **ornith:9b** | **thinking on**, temperature 0.2, 8,192 output cap | 6 | 6 | **5** | 49 |

\* Logged as 0. One program failed only because the rig ran it under
the Windows console code page and it printed a "greater or equal"
sign. That was the rig's fault and is fixed (`PYTHONUTF8=1`); rerun by
hand, the program works and prints a sensible answer.

## What went wrong, by kind

**qwen3.5:9b, thinking off.** All three plain-Python files had syntax
errors (mismatched brackets, a stray `except`). Two of three ezr
replies rambled to the output cap without closing the file. The
model's default presence penalty of 1.5 is a likely cause, since code
must repeat brackets and names; that was not tested, because the run
was dropped in favour of ornith.

**qwen3.5:9b, thinking on.** Three of four calls spent the whole
8,192 tokens reasoning and returned no file. An earlier single call
did the same in 227 s. Thinking on is unusable at this budget.

**ornith:9b.** No syntax errors, no runaway replies, three times
faster. The failures are ordinary bugs:

- treatment 1, step 2: `float('')` on an empty cell;
- treatment 1, step 3: an index past the end of a list;
- treatment 6, all three steps: `sys` used without importing it, and
  `csv(...)` called without the `ezr.` prefix.

One behaviour to watch: in treatment 6, **step 3 was a copy of
step 1** with only the docstring changed. It answered the wrong ask.
At low temperature, with "write as little new code as possible" in
the prompt, the model may copy instead of extend. A copy has few new
lines and so looks like perfect reuse. Line counts alone cannot tell
the two apart; the quality score must.

**ornith:9b, thinking on.** Five of six programs ran, at about the
same speed (thinking here costs a few hundred to 1,500 tokens, not
thousands). The one failure was a type error in treatment 1, step 2.
The copying seen with thinking off did not recur: the three ezr files
differ, are 13, 43 and 22 lines long, and step 3 calls `ezr.same` to
answer the "is it real or noise" ask, which is the reuse the
hypothesis predicts.

**But "ran" is not "right".** Two of the five that ran give a wrong
answer. Both step-3 programs test `overTime == "Y"` when the data
says `Yes`, so they find no overtime workers: one reports "0 people"
in each group, the other "not enough data for a statistical test".
Both exit with status 0. Only a scorer that checks the answer would
catch this.

## Where this leaves the choice

**ornith:9b with thinking on** is set in `rig/config.json`. It is the
only configuration tried that mostly produces running programs.

It is still six calls on one data set with one seed each: enough to
rank the configurations, not to predict a failure rate. The first
real batch should be watched for the same reason.

Not tried: a higher temperature, granite4.2:8b, any hosted model.

At about 50 s per call: about 7.5 hours for N = 3 (540 calls) and
about 25 hours for N = 10 (1,800 calls), one call at a time. Later
steps carry longer prompts, so expect somewhat more.

## With the scoring contract in the prompt

Later the same night the prompt gained a requirement: define a
function with a fixed signature so the scorer can call it
(`rig/contract.py`). Same six calls, ornith:9b, thinking on:

| treatment | step | skill | new lines | script ran | Q | baseline | note |
|---|--:|---|--:|:--:|--:|--:|---|
| 1 plain | 1 | remember | 49 | yes | 0.51 | 0 | |
| 1 plain | 2 | guess | 70 | no | 0 | 0 | tried to turn a hidden "?" cell into a number |
| 1 plain | 3 | certify | 40 | no | 0.66 | 0.5 | function works; its script part does not |
| 6 ezr | 1 | remember | 27 | no | 0 | 0 | gave ezr rows without the header row |
| 6 ezr | 2 | guess | 27 | no | 0 | 0 | same mistake, inherited |
| 6 ezr | 3 | certify | 18 | no | 0.55 | 0.5 | |

Three of six earned a real score, at about 49 s per call. The
contract asks more of the model, so fewer scripts run end to end than
without it (1 of 6 against 5 of 6). The two measures now disagree in
both directions, which is the point of having a scorer: a script can
run and be wrong, and a function can be right inside a script that
crashes. Use Q for quality; keep `ran_ok` only as a diagnostic.

The ezr programs are short and do call ezr (`Tbl`, `acquire`,
`ranker`, `ydist`), but misuse it. All of the failures are the
model's own; none traced to the rig.

## The retry fix, on a full ten-step climb

The first real run was paused after 11 calls: 3 of 5 late steps
returned no file (thinking used the whole output budget) and 3 of 8
files crashed on `from typing import list`. Two changes followed: one
fresh retry with thinking off when no file comes back, and plainer
signatures in the contract. One climb then ran on pom3a, treatment 1,
and was scored on the held-out 20%:

| step | skill | new lines | attempts | Q | baseline | scorer status |
|--:|---|--:|--:|--:|--:|---|
| 1 | remember | 28 | 1 | 0.69 | 0 | ok |
| 2 | guess | 46 | 1 | 0 | 0 | error |
| 3 | certify | 46 | 1 | 0.86 | 0.5 | ok |
| 4 | flow | 33 | 2 | -0.07 | 0 | ok |
| 5 | blame | 45 | 1 | 0 | 0 | error |
| 6 | justify | 24 | 2 | 0 | 0 | error |
| 7 | choose | 29 | 1 | 0.5 | 0.5 | error |
| 8 | fix | 68 | 1 | 1.0 | 0 | ok |
| 9 | spot | 58 | 2 | 0.04 | 0 | ok |
| 10 | race | none | 2 | 0 | 0 | no file |

Nine of ten steps returned a file (before: 2 of the 5 late steps).
The retry fired four times and rescued three. No `typing` errors.
Five programs scored without error; three beat their baseline
clearly. The remaining failures are ordinary bugs in the model's
code.

Cost: about 100 s of model time per call on average, so roughly 5 h
for one repeat of everything (180 calls) and 15 h for three (540).
