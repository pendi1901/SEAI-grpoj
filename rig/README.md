# rig: the experiment runner

Tooling for treatments 1 to 6. Written by an LLM (Claude) on Nov 16
2026; disclose that in the report. Nothing here is part of treatment 7,
and nothing here should be counted in the hand-written line totals.

**Tested only against a mock LLM.** No real model has been called, and
no data has been downloaded yet.

## What it does

For every (data set, treatment, trial) it climbs the ladder: ten LLM
calls in order, one per skill. Call i gets the background library, the
code from calls 1..i-1 of the same climb, and the one-line customer
ask. Each call:

1. gets its own new directory, `runs/<domain>/t<k>/trial<nn>/step<nn>/`;
2. receives only the data file, the library, and the earlier steps;
3. is refused if any `CLAUDE.md` sits at or above that directory;
4. has its prompt, reply, extracted file and run output saved there;
5. appends one row to `results/calls.csv` the moment it ends.

A call that fails (no code, a crash, a timeout, a backend error) is
logged with zeros and an error message. It is never dropped.

## Use

    python rig/test_run.py                  # want "failures: 0"
    python rig/run.py fetch                 # 3 csv files + ezr.py, ~4 MB
    python rig/run.py plan --trials 10      # what would run: 1,800 calls
    python rig/run.py go --backend claude --limit 10     # timing test
    python rig/run.py status --trials 10 --workers 8     # measured ETA
    python rig/run.py go --backend claude --trials 3 --workers 8
    python rig/run.py go --backend claude --trials 10 --workers 8

Raising `--trials` later keeps every finished call and only adds the
new trials. Stopping and restarting loses at most the calls in flight.
Narrow a run with `--domains hr` or `--treatments 5 6`.

## Before the first real run

1. **Pick a backend** in `config.json`. A backend is any command that
   reads a prompt on stdin and prints a reply.
   - `claude`: needs the `claude` CLI installed. Fill in `model`. Check
     how to switch off memory and user-level instructions in your
     version of the CLI, and add those flags to `cmd`. The runner
     checks for `CLAUDE.md` in the directory tree; it cannot see a
     user-level one in your home folder.
   - `ollama` (the default): see the next section.
2. **Install scikit-learn**, or treatments 3 and 4 will all crash.
3. **Run `fetch`.** It downloads from `timm/moot` and `timm/ezr`.
4. **Run the timing test**, then `status`, and decide N.

## Running on local Ollama

Chosen Nov 16 2026: a local model on the laptop's 8 GB RTX 5060. The
runner talks to Ollama over HTTP at `localhost:11434`. Tested against
a fake server only; Ollama is not installed on this machine yet.

Ollama runs in the Docker container `ollama`, with GPU
access, on port 11434. The model in the config is `ornith:9b`, with
thinking on; why is in `docs/model-trials.md`. The data and `ezr.py`
are already fetched. Still to install: `pip install scikit-learn`.

    python rig/run.py go --limit 10       # timing test
    python rig/run.py status
    python rig/run.py go --trials 3       # 540 calls; leave it overnight

What the runner does for you on this backend:

- **Stateless calls.** Each request carries the prompt and nothing
  else (no `context` field), so no call can remember another. That is
  the reset protocol; say so in Methods.
- **A big enough context window.** Ollama's default window is small
  and it drops the start of a long prompt without saying so. The ezr
  treatments send all of `ezr.py` plus the earlier steps. The config
  sets `num_ctx` to 16384, and any call whose prompt fills 95% of the
  window is flagged in the log's `error` column.
- **A seed per call**, derived from domain, treatment, trial and step,
  and logged. Trials differ; reruns of the same call do not.
- **Token counts** from the server, in the log.

Things to decide and check:

- **The model is provisional.** Fix it, and its settings, before the
  first real run and never change them partway.
- **Use one worker.** One GPU serves one call at a time.
- **Watch the first ten calls.** If `status` shows few programs
  running clean, or the log shows truncation flags, fix that before
  the long run: lower the window pressure by raising `num_ctx` (uses
  more GPU memory) or try another model.
- **If the 16k window does not fit in 8 GB**, Ollama moves part of
  the model to the CPU and calls get several times slower. `ollama ps`
  shows the split.

## What the log holds

`results/calls.csv`, one row per call:

| column | meaning |
|---|---|
| domain, data, treatment, library, reuse, trial, step, skill, ask | which call |
| backend, model, dir, when | proof of the reset protocol |
| new_lines | code lines in the new file (blank and comment lines not counted) |
| total_lines | new_lines plus the earlier steps of this climb |
| pct_new | 100 x new / total: the histogram's y-axis |
| got_code, ran_ok, error | did it reply with code; did `python stepNN.py` exit 0 |
| llm_secs, run_secs, prompt_chars, reply_chars, prompt_tokens, reply_tokens | cost (tokens on Ollama only) |
| seed | the seed sent with the call |

## Choices made here that the report must state

- **Ten steps**, one per skill: asks 1 to 10 of each requirements doc.
  Change `"asks"` in the config to use others.
- **One file per step.** The model may import earlier files and may
  not edit them. New code = the lines of the new file.
- **No-reuse treatments still see the earlier code** but are not told
  to reuse it. Flip `SHOW_PRIOR_TO_NO_REUSE` in `run.py` if the
  lecturer says otherwise.
- **The ezr treatment uses the Python `ezr.py`** from `timm/ezr`, not
  the Lua one in the course repo.
- **Each call is text in, text out.** The model writes a file; it does
  not get to run tools or look around.

## The scorer

`rig/score.py` gives every generated program one number, Q, following
the ten-skill table in the course's gloss10 page. Higher is better.

    python rig/test_score.py          # want "failures: 0"
    python rig/score.py --workers 8   # scores every call not yet scored

It reads `results/calls.csv` and writes `results/scores.csv` (domain,
treatment, trial, step, skill, q, status, detail). It runs on the CPU,
needs no LLM, and can be rerun at any time: scored programs are
skipped.

### The contract

A program that only prints cannot be graded. So the prompt now also
requires each step file to define one function, named after its skill,
with a fixed signature (`rig/contract.py`). The scorer imports the
file and calls that function on test cases it builds from the data.
Every program for one skill in one domain faces the same test cases.

| skill | the function must | Q | failure earns |
|---|---|---|--:|
| remember | return up to 5% of rows it judges best | 1 - median score of its rows / median score of random sets | 0 |
| guess | predict the first goal for held-out rows, 30 splits | 1 - its error / error of guessing the training mean | 0 |
| certify | say same or different for 200 pairs of samples | share it gets right | 0.5 |
| flow | say yes or no as each row arrives, 100 orders | 1 - chosen row's score / average score | 0 |
| blame | name the input columns behind bad rows | improvement when those columns are reset to good values, minus the same for random columns | 0 |
| justify | give a row's percentile and a reason, 20 rows | improvement over always answering 0.5 | 0 |
| choose | find the best row using at most 50 labels, 30 runs | win 1, tie 0.5, loss 0 against the best of 50 random rows | 0.5 |
| fix | recommend a change using allowed levers only, 20 rows | share of changes that are valid | 0 |
| spot | list suspect rows; 10 errors planted in 1,000 rows | hits in its first 20, divided by 20 (so 0.5 is perfect) | 0 |
| race | compare 3+ search strategies within 50 labels, 30 runs | win rate of its winner against random; invalid race = 0 | 0 |

"Score" is distance to the best possible goals, 0 best, 1 worst.
A missing function, a crash, a timeout (300 s) or an answer outside
the rules earns the failure value. The `status` column says which.

### Where this differs from gloss10, and why

These are my readings of a one-line-per-skill table. No scorer was
supplied with the course. State them in Methods, and check them with
the lecturer (open question 1).

- **blame** drops "rules" and takes column names only. Real data has
  no simulator to re-score a rewritten row, so the scorer estimates
  the new score from the 5 nearest real rows.
- **justify** hides the row's goals, or the percentile could simply
  be read off.
- **spot** plants errors 6 standard deviations from a column's mean
  in a numeric input, and uses 10 copies, not 30, to save time.
- **choose** and **race** search pools of 300 rows per run.
- **guess** uses 500 training and 100 test rows per split.
- Tables over 2,000 rows are sampled down to 2,000 (pom3a).
- **Levers** for fix come from `config.json` and are proposals.
- Q is clipped to the range -1 to 1.

### What the checks show

`test_score.py` grades three stand-in programs on a made-up table: a
sensible answer beats the baseline on all ten skills, a random or
constant answer does not, and a crash earns exactly the baseline.

## What it does not do yet

- **No Z rescaling, `same` tables or histograms.** Those read
  `calls.csv` and `scores.csv` and are the next piece.
