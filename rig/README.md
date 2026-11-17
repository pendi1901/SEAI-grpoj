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
   - `ollama`: needs Ollama and the model pulled. One GPU means use
     `--workers 1`.
2. **Install scikit-learn**, or treatments 3 and 4 will all crash.
3. **Run `fetch`.** It downloads from `timm/moot` and `timm/ezr`.
4. **Run the timing test**, then `status`, and decide N.

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
| llm_secs, run_secs, prompt_chars, reply_chars | cost |

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

## What it does not do

- **No quality score.** `ran_ok` only says the program ran. The Q
  scores in `docs/stats.md` need a separate scorer, not yet written.
- **No token counts**, only characters; the backends differ too much.
- **No `same` tables or histograms.** Those read `calls.csv` and are
  the next piece.
