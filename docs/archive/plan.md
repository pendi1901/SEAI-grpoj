# The plan: what to do, who does it, how long

Written Mon Nov 16 2026. Final report due **Mon Nov 30, start of
class**: 14 days. This file is the instructions; the reasons are in
[brief.md](brief.md), [stats.md](stats.md), [runs.md](runs.md),
[domains.md](domains.md).

It assumes nothing is built yet. If the team already has requirements
docs, a tagged ladder or a pre-registered claim from the Nov 9
deliverable, strike those lines.

Time figures are estimates, not measurements. Step 4 below replaces
them with a real number in ten minutes.

## 1. Who does what

### Must be done by a human on the team

These cannot be handed to an LLM, by rule or because they are marked
as human work.

| # | task | why it is yours |
|--:|---|---|
| H1 | **Treatment 7: write all ten skills by hand, for each of the three data sets.** One run each, 30 steps. Tag each step. | Lecturer (A21): LLM-built code here is "out of court". An LLM may point you to material or write a tutorial; it may not write the code. |
| H2 | **Get the three requirements docs okayed by the lecturer.** | The okay is a rubric condition. |
| H3 | **Fix the domain facts**: which Health file; which columns are levers (changeable) in each data set; how errors are injected for the spot skill. | These are judgment calls the scorer depends on. Write them down before any run. |
| H4 | **Confirm the pre-registered claim** exists, dated before the code. If it does not, write it now and say so in the report. | The report is marked against it. Inventing it after results loses marks. |
| H5 | **Read the LLM's output and catch its errors.** Keep a list. | AI disclosure, 3 marks: "zero caught errors reads as zero checking". |
| H6 | **The talk**: discuss with the lecturer the week before, share Google Slides (public, editable by timm@ieee.org), present in person with the whole group on stage. | 15 marks; the discussion alone is 2, all or nothing. |
| H7 | **The verdict.** Which hypothesis won, per domain and overall. | You must be able to explain everything submitted (policies.md). |
| H8 | **Ask the open questions** on Discord: is the gloss10 Q table required; does N of 3 to 5 earn full credit (Q22); do no-reuse treatments see earlier code. | Each answer changes the workload. |

### Can be handed to an LLM (disclose it in the report)

Course policy allows and encourages AI use for projects, with
disclosure. None of this is treatment 7.

| # | task |
|--:|---|
| L1 | First draft of the three requirements docs (20 asks each, customer words, skill-tagged). You edit and own them. |
| L2 | The **runner**: makes a fresh directory per trial, calls the LLM headless, saves the code, logs one csv row per call, resumes after a crash. |
| L3 | The **scorer**: runs each generated program and computes its score. |
| L4 | Treatments 1 to 6 themselves. The LLM writing code *is* the experiment. |
| L5 | Line counting, the `same` and rank tables, the histograms. |
| L6 | The `acmart` LaTeX skeleton, tables, figure placement, a slides draft. |

Keep L2, L3 and L5 in their own directory (say `rig/`), apart from the
hand-written skills. Otherwise LLM-written lines pollute the
treatment 7 line counts and the claim that it was hand-built.

### Can be split across teammates

- One domain's requirements doc each.
- Treatment 7: one person builds domain 1 (the expensive one). The
  second and third domains should be mostly reuse; others take those.
- Report: one person on Methods and Results, one on Requirements and
  Discussion.

## 2. Does it really need that much compute?

**No.** Three separate things get called "runs".

| what | how many | where it runs | cost |
|---|---|---|---|
| LLM calls that write code (treatments 1-6) | 3 data sets x 6 treatments x 10 skills x N | hosted API, or a local model | this is the "46 hours" |
| scoring each generated program | same count | laptop CPU | minutes to an hour or two in total |
| treatment 7 | 30 steps, once | your hands | days of your time, no compute |

    N = 3    540 calls
    N = 5    900 calls
    N = 10   1,800 calls

Nothing here trains a model. The data sets are small (1,470 to 20,000
rows). The 46 hours another team reported matches 1,800 calls done one
after another at about 90 seconds each. It is waiting time, not heavy
computing, and most of it disappears if calls run side by side.

## 3. Two ways to run it, and the time each takes

Checked on this laptop on Nov 16: RTX 5060 Laptop GPU with 8 GB,
28 logical CPU cores, 32 GB RAM, Python 3.14, Docker and WSL present.
**Not installed:** `claude` CLI, Ollama, Lua, scikit-learn, cloc, LaTeX.

### Option A: hosted model (recommended)

`claude -p` or an API call with empty history. The laptop only sends
requests, so its GPU does not matter.

| N | calls | one at a time (~90 s) | 8 at once |
|--:|--:|--:|--:|
| 3 | 540 | ~14 h | ~2 h |
| 5 | 900 | ~23 h | ~3 h |
| 10 | 1,800 | ~45 h | ~6 h |

Limits: a subscription plan will hit rate caps and stretch this over
more days; an API key costs money per token. Rough size of N = 10:
1,800 calls at perhaps 8,000 tokens in and 1,500 out each, so about
14 million input and 3 million output tokens. Check the current price
before committing.

### Option B: local model on the 8 GB GPU

Free, but slower and weaker. 8 GB holds a 7B-class coding model at
4-bit; a 14B model spills into system RAM and slows sharply. One GPU
serves about one call at a time, so there is no parallel speed-up.

| N | calls | at ~45 s per call |
|--:|--:|--:|
| 3 | 540 | ~7 h |
| 5 | 900 | ~11 h |
| 10 | 1,800 | ~23 h |

That is one or two overnight runs. The catch is quality: a small model
will produce more programs that crash. Crashes are scored at the
baseline and are a legitimate finding, but if most runs fail, the
tables say little about reuse. Name the model and its size in Methods
either way.

### Which

Use A if any budget or plan access exists; use B as the fallback or
for the dry run. Either way do N = 3 first, then extend the same
trials to 10. Never restart from zero.

## 4. Get a real number first (10 minutes)

Before planning further: make one call for one skill on one data set,
with the real prompt, and time it. Do it ten times. Multiply.

    ETA hours = calls x seconds per call / 3600 / parallel workers

If N = 10 does not fit before Nov 28, run N = 5 and say so in Methods.
Under the rubric as written that costs Results marks; Q22 asks whether
the lecturer will waive that.

## 5. Day by day

Dates assume the talk is Mon Nov 23. If the talk was today, drop the
talk lines.

| days | you (human) | handed off |
|---|---|---|
| **Mon 16 - Tue 17** | H8: post the open questions. H3: pick the Health file and the levers. H4: confirm the claim. Email the lecturer to book the pre-talk discussion (H6). | L1: draft the three requirements docs. Install scikit-learn, cloc, a LaTeX route (Overleaf needs no install), and the `claude` CLI or Ollama. |
| **Wed 18** | Edit the requirements docs; send for the okay (H2). Start treatment 7 on domain 1: skills 1-3, tag `step1`..`step3`. | L2: build the runner. Step 4 timing test. |
| **Thu 19 - Fri 20** | Treatment 7, domain 1: skills 4-10, tagged. Tests and one-command demos as you go. | L3: build the scorer. Dry run: 1 data set x 6 treatments x N = 1. Fix what breaks. |
| **Sat 21 - Sun 22** | Treatment 7 on domains 2 and 3; record lines reused, changed, new (the transfer number). Meet the lecturer about the talk. Write the slides. | Launch N = 3 on all three data sets. L5: first tables and histograms. |
| **Mon 23** | **Give the talk**: claim, what ran, verdict so far. | Extend runs toward N = 10 overnight. |
| **Tue 24 - Wed 25** | H5: read a sample of generated programs in each treatment; log the errors found. Do the ezr tuning if ezr loses (brief.md section 9). | Runs finish. Final tables, histograms, Z-scaled comparison. |
| **Thu 26 - Sat 28** | Write Discussion and the AI disclosure. Decide the verdict per domain and overall (H7). | L6: LaTeX skeleton; fill Methods and Results tables. |
| **Sun 29** | Check: 6 to 9 pages, repo URL on page one, repo public, tags present, every demo runs from the README in one command, both hypotheses verbatim. | |
| **Mon 30** | Upload the PDF to Moodle before class. | |

## 6. Your own hours

The compute is small. The human time is the real cost.

| task | estimate |
|---|--:|
| Treatment 7, domain 1 (about 330 lines in the reference build, plus tests and demos) | 15-25 h |
| Treatment 7, domains 2 and 3 | 3-6 h each |
| Requirements docs: edit, lecturer round trip | 4-6 h |
| Checking LLM output, error log | 4-6 h |
| Talk: slides, rehearsal, lecturer meeting | 5-8 h |
| Report writing | 12-18 h |
| **Total** | **about 45-75 h**, across the team |

With three people that is 15 to 25 hours each over two weeks.

## 7. If time runs out, cut in this order

1. N from 10 to 5, then to 3 (the floor; half the Results marks).
2. Skip ezr self-tuning; report that untuned ezr lost.
3. Shorten the report toward 6 pages.

Do not cut: any of the three domains, treatment 7, the `same` tables,
the reset protocol, or the AI disclosure. Each of those is named in
the list of ways to lose marks.
