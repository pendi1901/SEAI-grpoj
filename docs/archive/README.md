# Archive

Documents that described earlier stages of the project. Kept for the
record and for the report's history; none of them describes the current
set-up. The run outputs they cite were removed from the working tree on
Nov 18 2026 and are kept at the git tag `archive/first-runs`:

    git checkout archive/first-runs -- results-gemini runs-gemini

| file | what it was |
|---|---|
| `plan.md` | the Nov 16 day-by-day plan, before the lecturer's later answers |
| `runs.md` | call counts and time estimates for local Ollama runs |
| `model-trials.md` | how the model was chosen: qwen3.5, ornith (Ollama), then Gemini |
| `results-n1.md` | the Ollama N = 1 run (prompt v1): 81 of 180 skills worked |
| `results-gemini-n1.md` | the Gemini N = 1 run (prompt v2): 138 of 180 skills worked |

Two numbers in those results changed after they were written: the
Nov 18 audit found that the scorer rejected numpy integers, which
wrongly failed 4 scikit-learn programs (1 in the Ollama run, 3 in the
Gemini run). The archived tables were not rescored.
