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

## Where this leaves the choice

ornith:9b is clearly the better of the two. One working program in
six is still low, and it is six calls, on one data set, with one
seed each: enough to rank the models, not enough to predict a
failure rate.

Not yet tried: ornith with thinking on; ornith at a higher
temperature (to reduce copying); granite4.2:8b; any hosted model.

At 43 s per call: about 6.5 hours for N = 3 (540 calls) and about
21.5 hours for N = 10 (1,800 calls), one call at a time.
