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

## Prompt versions

| version | used by | change |
|---|---|---|
| 1 | Ollama N = 1 run, in `runs/` and `results/` | |
| 2 | Ollama run stopped at 144/180 (`runs-v2/`); Gemini N = 1 run (`runs-gemini/`, `results-gemini/`) | states the data file's row count and says not to hard-code one |
| 3 | not yet run; configured for `runs-gemini-v3/` and `results-gemini-v3/` (Gemini), `runs-v3/` (Ollama) | clearer contract, plus one repair round (below) |

Never pool results from two prompt versions. To report on an older
version, run `score.py` and `report.py` with a config whose `runs` and
`log` point at its folders. Each config's `prompt_version` sets the
version; it is also logged on every call from version 3 on.

## Prompt version 3

Built Nov 17 2026 after the error breakdown of the first two runs. Not
yet piloted or run.

**A clearer contract.** The prompt now also shows:

- the header and the first two rows exactly as the function receives
  them (floats and strings, already parsed);
- every text column and its values, e.g. `overTime (No, Yes)`;
- each skill's rules and what breaking them costs (`RULES` in
  `rig/contract.py`): the 5% cap, the shared 50-label budget, "p from
  0 to 1, not a percentage", no state kept between flow calls, and so
  on. These restate the signed-off assessment sheet. They describe the
  data and the harness, never how to solve a skill.

**One repair round.** After a file comes back, the runner calls its
skill function on a sample of the *training* data, with the scorer's
own rules, sizes and label budget and only fewer repetitions
(`score.py --check`). If that fails, the model gets one more call: the
original prompt, its file, and the error. The corrected file replaces
the first, which is kept as `first_try.py`. Then the run moves on;
there is no second repair.

- **Never the test suite.** The check reads the training file for
  both halves, and a test confirms it is never passed the test file.
- **No local paths leave the machine.** The error shown keeps only
  the generated file's own lines and library lines, each cut to a
  bare file name, and drops every line of the harness.
- **Same rule for every treatment.** Logged per call: `check_before`,
  `check_after`, `repaired`, and the extra call in `attempts`,
  `llm_secs` and the token counts.
- **What it changes for Methods:** the treatments become "an LLM with
  one repair round on training data". Treatment 7 (hand-written) also
  runs its code before submitting, so this brings the LLM treatments
  closer to it, not further. New lines are counted on the final file.

Cost: one extra call for each file that fails its check. On the last
Gemini run that would have been about 40 of 180 calls.

## The scorer

`rig/score.py` grades every generated program on a fixed test suite.
**How each skill is judged is defined in `docs/assessment.md`**, which
a human on the team must agree before any large run. This section is
only the mechanics.

    python rig/test_score.py          # want "failures: 0"
    python rig/score.py --workers 8   # scores every call not yet scored

It runs on the CPU, needs no LLM, and can be rerun at any time: scored
programs are skipped. To rescore after a rule change, delete
`results/scores.csv` and `results/cases.jsonl` and run it again; the
generated programs are kept, so no model calls are needed.

Files it writes, beside `results/calls.csv`:

| file | holds |
|---|---|
| `scores.csv` | one row per program: Q (mean over its test cases), number of cases, status, detail |
| `cases.jsonl` | one line per program: the per-test-case numbers, plus `fix_helps` for the fix skill |

### The 80/20 split

Each data set is split once, with the seed in `config.json`, into
`data/<name>.train.csv` (80%) and `data/<name>.test.csv` (20%).
Treatments are given the training file only. The scorer builds its
test cases from the test file, seeded by domain and skill, so every
treatment and every trial faces the same test suite.

### The contract

A program that only prints cannot be graded. So the prompt requires
each step file to define one function, named after its skill, with a
fixed signature (`rig/contract.py`). The scorer imports the file and
calls that function.

A missing function, a crash, a timeout (300 s) or an answer outside
the rules earns the skill's baseline on every test case. The `status`
column says which: `ok`, `invalid`, `error`, `timeout` or `no_code`.

### Where this differs from gloss10

No scorer was supplied with the course; these are readings of a
one-line-per-skill table. State them in Methods.

- **One fixed 80/20 split** replaces gloss10's repeated splits, as
  the lecturer's Nov 16 notes describe.
- **choose** fails to 0, not 0.5 (decision A in the assessment sheet).
- **fix** keeps the course's number and adds "fix: helps" (decision B).
- **blame** takes column names only, no rules; a rewritten row's new
  score is estimated from its 5 nearest training rows.
- **justify** hides the row's goals, or the percentile could be read
  off.
- **spot** plants errors 6 standard deviations out in a numeric
  input, in 10 copies rather than 30.
- **choose** and **race** search 150 test rows per run.
- Training rows are capped at 2,000 and test rows at 400 (pom3a).
- Each test case's number is clipped to the range -1 to 1.
- **Levers** for fix come from `config.json` and are proposals.

### What the checks show

`test_score.py` grades three stand-in programs on a made-up table: a
sensible answer beats the baseline on all ten skills, a random or
constant answer does not, and a crash earns exactly the baseline on
every test case.

## The report

    python rig/test_report.py         # want "failures: 0"
    python rig/report.py              # writes results/report.md, results/fig/

Per domain: the % new code histogram; treatments ranked per skill on
the test suite; new lines and Q per step; and Q rescaled to Z within
each domain and skill for comparison across skills. Ranks use the
lecturer's Python `same` with all three tests. It works on a partial
run. If `results/t7.csv` exists (columns `domain,step,new_lines`),
treatment 7 is drawn as a reference line.
