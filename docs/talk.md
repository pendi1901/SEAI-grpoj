# Next week's talk: outline and checklist

Rules (lecturer, Q25 and A28, Nov 17): **mandatory**; 12 groups, six per
hour, **10 minutes each** including the machine change; **at most 10
slides**, fewer is better; "very rough and ready ... charts. yes.
beautiful powerpoint not". Marks are lost for not presenting or for
running over time. From the task-talk rubric in `gproj.md`: the claim
stated first; `same` on every comparison shown; an honest verdict;
**discussed with the lecturer the week before (2 marks, all or
nothing)**; Google Slides, public, **editable by timm@ieee.org**; given
in person with the whole group on stage.

Aim for 7 slides and 7 minutes of speaking.

## Slides

Every number below comes from `results/report.md`, produced by
`rig/report.py`. Regenerate it after the final run so the slides match
the repo.

| # | slide | content | source |
|--:|---|---|---|
| 1 | The bet | Both hypotheses, verbatim, and their win conditions, as pre-registered. One line: three clients, seven treatments. | `docs/brief.md` section 3 |
| 2 | Set-up | Three domains (agile process, project health, staff retention), 1,000 random rows each, 80/20 split, one shared test suite. The seven treatments as a 3 x 2 grid plus T7. Model, fresh call per step, N. | `docs/brief.md`, `rig/README.md` |
| 3 | What it cost (A28) | One table, all seven treatments: programs, functions that work, beat the dumb baseline, new LOC, tokens, dollars, clock time. | report: "Competency and cost", all domains |
| 4 | Is the model competent? (A23) | Functions that work, per treatment, as a bar chart. Earlier local Ollama runs worked far worse, the reason for switching to Gemini. | report: competency columns; `results/report.md` |
| 5 | New code, seven ways | Bar chart of median new lines per step per treatment, labelled with `same` ranks. | report: "New lines, pooled" |
| 6 | Quality, seven ways (gloss6) | Per-skill table across T1-T7 as a heatmap: mean Q and rank per cell. "Treatments that share a rank are not distinguishable." | report: "Per skill, on the test suite" |
| 7 | Verdict so far, and next | Which hypothesis the evidence leans to, per domain and overall; the % new code artefact in one line; the decision (persevere / re-plan / descope) and what runs next. | `results/report.md` |

Optional eighth slide only if time allows: one failure worth showing
(for example, the scikit-learn programs that never encoded text
columns), since "failures are findings".

## Checklist before the talk

| done? | what | who |
|:--:|---|---|
| [ ] | Click the acknowledgement on the lecturer's Discord post ("expecting 12 clicks") | anyone |
| [ ] | Book a lecturer appointment this week and discuss the talk (2 marks) | anyone |
| [ ] | Write treatment 7 (`t7/README.md`), at least for one domain, so slides 3, 5 and 6 can show all seven | team, by hand |
| [ ] | Run prompt v3 on Gemini at N = 1 with the 1,000-row cap (about $0.50, under an hour) | anyone |
| [ ] | `python rig/t7.py`, then `python rig/score.py`, then `python rig/report.py` | anyone |
| [ ] | Build the slides in Google Slides; share publicly and as editable with timm@ieee.org | team |
| [ ] | Rehearse once with a timer: finish well inside 10 minutes | whole group |

If T7 is not ready, present T1-T6 and say so on slide 7: a declared gap
costs less than a hidden one.

## What not to claim

- Any difference that `same` does not certify.
- That falling "% new code" bars show reuse: they fall for every
  treatment (see the results write-ups).
- Results pooled across prompt versions or models.
