# How many runs, and how long

The repo gives no run count and no time estimate. It gives the design;
the arithmetic below follows from it. The "46 hours" figure is hearsay
from another team; the last section shows it is plausible and what it
most likely measured.

## Counting LLM calls

One **trial** = one climb of the whole ladder, for one treatment, in
one domain. A climb is S calls in sequence, because the prompt for
skill i+1 includes the code for skills 1..i (uproj.md: "supply the
background library, the code for skills 1..i, and the one-line
requirement").

    calls = 3 domains x 6 LLM treatments x S steps x N trials

| N | S = 10 (one step per skill) | S = 20 (one step per ask) |
|--:|--:|--:|
| 3 (floor, half marks) | 540 | 1,080 |
| 10 (full marks) | 1,800 | 3,600 |
| 20 ("the dream") | 3,600 | 7,200 |

Whether a ladder has 10 steps or 20 is not stated (open question 3).
The worked example and the ten-skill table both use 10.

Treatment 7 adds one handwritten run of all ten skills per data set:
30 steps by hand, no repeats (lecturer, Discord A21, Nov 16). With a
single run, treatment 7 contributes one number per cell, so `same`
cannot be applied to it; show it as a reference line beside the six
LLM distributions.

## Counting scoring runs

Each generated program is then scored. Under the gloss10 protocols that
is 30 train/test splits, or 100 arrival orders, or 200 sample pairs, or
30 runs at 50 labels, per program. That is CPU work on small tables and
is cheap next to the LLM calls, provided the generated code is not
quadratic on pom3a's 20,000 rows. Cap rows (ezr's own `cap` is 1024)
or sample.

## Why 46 hours is believable

    1,800 calls x 1.5 min = 45 hours

So 46 hours matches N = 10, S = 10, run one call at a time, at about
90 seconds per headless call. If the other team ran a local model, that
time is GPU time. With a hosted API it is wall-clock waiting, not GPU.

## Cutting the wall-clock time

- **Trials are independent.** Different trials, treatments and domains
  share nothing by design (fresh directory each). Run them in parallel:
  eight workers turn 45 hours into about 6. Only the S steps *inside*
  one climb must stay in order.
- **Run N = 3 first.** It proves the pipeline end to end and is the
  floor. Then extend the same trials to 10; never throw runs away.
- **Make the runner resumable.** Skip any (domain, treatment, trial,
  step) already in the log. A crash at hour 30 should cost one call.
- **Log cost per call** (seconds, tokens). It is evidence, and it tells
  us early whether N = 10 fits before Nov 30.

## The reset protocol (what Methods must document)

Per trial:

1. make a new empty directory;
2. copy in only: the background library for that treatment, the data
   file, the code for skills 1..i from *this* trial, the one-line ask;
3. one headless call (`claude -p`, or the API with empty history);
4. memory off, no CLAUDE.md anywhere up the directory tree, no project
   context;
5. record the command, model id and directory in the log.

For the no-reuse treatments (1, 3, 5), uproj.md says two things: "in
every treatment ... supply ... the code for skills 1..i", and "ask an
LLM for each skill cold, one fresh prompt per skill". The reading used
here: prior code is supplied, the instruction to reuse it is not. That
is open question 6.

A new chat window does not count as a reset. Shared context makes N
trials into one.

## Measuring new code

Per step, from tags: `git diff --stat step2..step3`, or cloc per tag.
The histogram's y-axis is **% new code**, x-axis is step, one line per
treatment. It must be reproducible by a stranger from the tags alone.

With N trials x 6 treatments x 3 domains, the tagged history in the
main repo can only be one climb (treatment 7, ours). Generated climbs
need their own storage with the same per-step diff recorded. How the
lecturer wants those tagged is open question 5.
