# What the repo does not settle

Checked against `txt/seai26f` at `5fb51c8` (Nov 16 2026, up to date
with origin). Anything said only in class or on Discord is not in the
repo and is not in these notes. Ask on Discord or by email
(timm@ieee.org) and write the answer, with its date, under each item.

## Things heard, and what the repo actually says

| heard | in the repo? |
|---|---|
| "we have to include the number of runs" | **Yes.** N must be declared in Methods (5 marks) and sets the Results marks: N>=10 full, N=3 half. |
| "it took 46 hours of GPU runtime" | **No.** No time or GPU figure anywhere. It is consistent with 1,800 serial calls at about 90 s each ([runs.md](runs.md)). |
| "statistics from today's gloss, reported after every run or task" | **Partly.** `same` on every comparison is in the rubric. gloss6 got new diagrams today for cohen, cliffs, ks and ranks. gloss10 (today's page) defines a Q per skill and a Z rescaling. Nothing in the repo says "after every run". |
| "the human part, the 7th task" | **Yes, as treatment 7**, not a task: we write every skill by hand with maximum reuse. It is the control. |
| "grads have more stipulations" | **Yes.** Three domains, one codebase, pre-registered claim, transfer evidence, 6-9 pages, initial deliverable, task talk. |

## Answered by the lecturer

Relayed from the class Discord on Nov 16 2026 (pasted by a team
member; not in the course repo).

- **A21, treatment 7.** "one handwritten run of all ten skills." So
  N = 1 for treatment 7, per data set. This settles question 4 below,
  and "all ten skills" points to a ten-step ladder (question 3), though
  that was not the question asked.
- **A21, LLM help in treatment 7.** "LLM as a search tool 'where is
  the stuff relating to xxxx or write me a tutorial with examples on
  how to use a decision tree', is ok. but LLM auto assembly (please
  build me that bit) is out of court." So: finding things and
  tutorials are allowed; any generated code going into treatment 7 is
  not. Debugging help was asked about and not answered directly; the
  safe reading is that an LLM may explain an error but may not write
  the fix. Log every LLM use in treatment 7 for the AI disclosure.
- **Stats link.** `github.com/timm/ezr/blob/main/ezr.py`, the stats
  section. A Python `same` exists; see [stats.md](stats.md). This
  removes the "Lua only" tooling gap and bears on question 8.

Asked, no answer seen yet:

- **Q22.** "Will we still get full credit for 3-5 repeats?" Until
  answered, the rubric stands: N >= 10 full, N = 3 half.

## Questions to ask

1. **Is the gloss10 Q table now required?** The rubric (uproj.md) asks
   only for new-code histograms and `same` tables. gloss10 says "the
   project scores ten skills" and describes a scorer and a "harness",
   and "the analysis re-expresses Q as Z". No scorer code is in the
   repo. Do we write our own scorer to that table, or is one being
   handed out?

2. **Z: pooled over what?** "Z within each domain and skill" gives no
   formula. Pool all treatments and trials for that (domain, skill)?

3. **Ten steps or twenty?** Twenty asks, ten skills. Is the ladder ten
   steps (one per skill) or twenty (one per ask)? It doubles the run
   count.

4. ~~What is N for treatment 7?~~ **Answered (A21): one handwritten
   run of all ten skills.**

5. **How are generated climbs tagged?** "Histograms derivable from the
   repo's tags" is clear for one ladder. For 6 treatments x N trials
   x 3 domains, do we tag every climb, or store per-step diffs in a
   results directory?

6. **Do no-reuse treatments see the earlier skills' code?** uproj.md
   says both "supply the code for skills 1..i" in every treatment and
   "ask for each skill cold".

7. **Which treatment set is current?** uproj.md: seven (three libraries
   x reuse yes/no, plus a human). `docs/review/w8.md`: "nine systems"
   (no hints / timm's toolkit / scikit-learn x all at once / one at a
   time with reuse / one at a time with revision). These notes follow
   uproj.md because gproj.md points to it.

8. **Is the ezr treatment Lua or Python?** Treatments 1-4 are Python.
   ezr in this repo is Lua (`src/ezr-lua/`); `src/101.py` is 51 lines.
   Is treatment 5/6 the Lua ezr, or a Python ezr from elsewhere?

9. **Which Health file?** There are 35. One as the domain, the rest as
   a robustness check?

10. **Is the HR table acceptable given its goals?** Goals are tenure;
    `attrition` is an input column. Does a wish list about attrition
    fit, or should the asks be about tenure?

## Things about our own status only the team knows

- Was the Nov 9 initial deliverable handed in, and were the three
  requirements docs okayed by the lecturer? The okay is a condition
  of those 2 marks and of the final Requirements marks.
- Is our task talk on Nov 16 or Nov 23? "Discussed with the lecturer
  the week before" is 2 marks, all or nothing.
- Was the claim written down before any code? The final report is
  marked against that pre-registered text.
- Is there already a team repo with `step` tags? If so, these notes
  belong beside it, not in a second repo.

## Tooling gaps found on this machine

- No `lua` or `luajit` installed, so `ezr.lua` cannot run here yet.
  `same` is available in Python from `timm/ezr` `ezr.py`, which needs
  Python 3.12+ (it uses `type` aliases); 3.14 is installed.
- No GitHub CLI. This repo is local only; it has no remote.
