# Gemini run: N = 1, three domains, six LLM treatments

Run Nov 17 2026 on `gemini-3.1-flash-lite` through the Gemini API,
prompt version 2, code at commit `903ce03`
(`results-gemini/run-commit.txt`). 180 calls, about 14 s each, about 45
minutes. 1.00M input and 0.12M output tokens: about $0.43 at Google's
paid rates. Scored on the held-out 20% under the signed-off
[assessment.md](assessment.md). Full tables: `results-gemini/report.md`;
figures: `results-gemini/fig/`. Treatment 7 (hand-written) is not done.

## Against the Ollama run

The Ollama run ([results-n1.md](results-n1.md)) used `ornith:9b` and
prompt version 1, so model and prompt both differ. Read this as two
separate runs, not a controlled comparison of models.

| | gemini-3.1-flash-lite | ornith:9b |
|---|--:|--:|
| returned a file | 180 of 180 | 178 of 180 |
| demo script ran | 152 (84%) | 66 (37%) |
| skill function scored without error | 138 (77%) | 81 (45%) |
| seconds per call | about 14 | about 96 |
| cost | about $0.43 | $0 |

Function success by treatment, Gemini: T1 27/30, T2 27/30, T3 16/30,
T4 19/30, T5 25/30, T6 24/30.

## What can be claimed

Only differences that `same` certifies, on pooled values (30 per
treatment) or per-skill test cases. Per-step cells hold one value each.

1. **New code per step, pooled (median lines, rank):** T5 ezr 35 (0),
   T6 ezr+reuse 36 (0), T4 sklearn+reuse 42 (1), T3 sklearn 46 (2),
   T2 plain+reuse 48 (2), T1 plain 52 (3).
   - The ezr library needed the least new code, as in the Ollama run.
   - **Unlike the Ollama run, the reuse instruction now cut code**
     within plain Python (52 to 48) and within scikit-learn (46 to 42),
     each certified by `same`. On top of ezr it added nothing (35 and
     36 share a rank).
2. **The reuse instruction was followed far more.** Files at steps 2
   to 10 that import an earlier step: T2 85%, T4 77%, T6 55% (Ollama:
   22%, 69%, 44%). The no-reuse treatments: 0% in both runs.
3. **Quality (Q rescaled to Z, pooled over domains and skills):** T1,
   T2, T5 and T6 share rank 0; the two scikit-learn treatments, T3 and
   T4, share rank 1. Reuse did not lower quality in any library.
4. **The scikit-learn treatments lose largely by crashing.** Their
   guess programs passed text columns ("Yes", "poisson") straight to
   scikit-learn without encoding them, and failed in HR and health.

## What this says about the hypotheses

With a model that mostly works, the evidence leans to the Timm
hypothesis on code size: both a factored library (ezr) and an
instruction to reuse earlier steps reduced new code, and neither cost
quality. Two limits stop it being a clean win:

- **The course's histogram still cannot show it.** "% new code per
  step" falls for every treatment as the denominator grows; in all
  three domains the six lines fall together (`results-gemini/fig/`).
  The reuse effect is visible only in absolute new lines.
- **New lines per step still rose slightly from early to late steps**
  (for example T1 49 to 56, T6 33 to 51), because the later skills are
  bigger tasks. So the "bars fall" test is confounded by skill order;
  the comparison that holds is reuse against no-reuse at the same
  steps.

## Skills that still cannot separate treatments

| skill | what happened |
|---|---|
| remember | the same score for all six in health (0.73) and process (0.69): sorting by the visible goals is a full answer |
| race | 2 working programs of 18 (health T2 0.43, HR T4 0.42); the rest broke the rules or crashed |
| spot | 0.50 (perfect) or near 0; many treatments 0 |

## Checks made on these numbers

- One program (process, T3, choose) ran past the 300 s limit and was
  scored twice by two overlapping scoring runs; the duplicate row was
  removed. Q unaffected: a timeout earns the baseline.
- Fix programs that scored 0 while "ok" returned an empty change
  (`{}`); the contract requires at least one change, so 0 is correct.
- Justify programs at -1.00 answered 0.0 for every row, where the true
  percentile was 0.73 to 0.95: they ranked the row by its goals, which
  are hidden.

## Errors in the LLM's code worth citing in the AI disclosure

- scikit-learn programs that did not encode text columns.
- Justify programs that read the hidden goal cells and returned 0.
- Fix programs that recommended no change at all.
- A choose program too slow to finish in 300 s.

## Caveats

N = 1; one model; one 80/20 split; our reading of gloss10's scoring.
The two runs differ in prompt version as well as model. Whether
per-test-case numbers can stand in for N >= 10 repeats is open
question Q22. At about $0.45 and 45 minutes per repeat, N = 10 is now
affordable.
