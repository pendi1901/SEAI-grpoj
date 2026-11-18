# Lecturer's project notes, Nov 16 2026

Posted by the lecturer after class and relayed by a team member. Marked
by him as "very important". Not in the course repo. Quoted where the
wording matters; the right-hand column is what each note changes here.

Appointment slots are open this week (link in the Discord post). "Now is
the time to ask questions."

## Before doing big runs with LLMs

| the note | what it means for us | status |
|---|---|---|
| "work thu each task and ask the LLM how would we assess this one? see if you agree with its methods. dont go on until you do." | A human on the team must read how each of the ten skills is scored and agree, before any large run. | [assessment.md](assessment.md) is the sheet to read and sign off. **Not yet agreed. No big run until it is.** |
| "get to the point of being able to collect numbers on (e.g.) an 80% train and 20% test suite. then for the 6 treatments you'll have 6 sets of numbers you can compare with my stats." | Split each data set 80/20. Treatments work from the 80%. Numbers come from the 20%. Six treatments give six sets of numbers; compare them with `same`. | Being built into the runner and scorer. |
| "do treatment T7. i.e. you won't be able to understand all the decisions within the automatic till you do the manual." | Do the hand-written skills early, not last. They are how we learn what the scorer should reward. | The team's job. Not started. |

## When making training and test sets

| the note | what it means for us | status |
|---|---|---|
| "pass the SAME test suite to each treatment" | One fixed test set per domain, and the same test cases for every treatment and trial. | The scorer already seeds its test cases by domain and skill, so every program faces the same cases. The 80/20 split makes the test rows fixed as well. |

## Regarding the Lua

| the note | what it means for us | status |
|---|---|---|
| If Lua "is not your friend, then jump to python, which you can auto-gen via LLMs (checking the test cases, of course)". Stats in Python: `timm/ezr` `ezr.py`, lines 321-359. | Python ezr is allowed for the ezr treatments, and for the statistics. | Already the case: treatments 5 and 6 are given `ezr.py`, and `rig/report.py` calls its `same`. |

## Cost

| the note | what it means for us | status |
|---|---|---|
| "set a max budget per person equal to the cost of a textbook. say $100. ... DO NOT EXCEED THAT BUDGET. If you blow $$$ then just stop and report on the surprising result that this simple task blew away LLMs" | Declare a budget. Stop at it. Running out is a reportable result. | Team decision (Nov 16): run on local Ollama models. Money cost is zero; the budget is GPU hours. Report cost as hours and tokens. |
| "consider not using the latest and greatest model" | Cheaper models are acceptable, even encouraged. | A local 9B model (`ornith:9b`) is as cheap as it gets. State it. |
| "if all hell breaks loose with cost, cut back to one domain and 1 repeat. with e.g. auto93 that will still generate say 80 test cases for 6 treatments." | There is an approved fallback: one domain, one repeat, where the 20% test set supplies the numbers. | Note the arithmetic: auto93 has 398 rows, and 20% is 80. So "test cases" means **test rows**, and the six sets of numbers are per-test-row results. This is how one repeat can still feed `same`. |

## What this changes in our design

1. **The numbers that go into `same` can come from test rows, not only
   from repeated trials.** With one climb per treatment, each skill
   still yields a list of per-row results on the test set (errors,
   scores, hits), one list per treatment. That is a far cheaper route
   to statistics than N = 10 climbs. Ask the lecturer whether this
   replaces the N >= 10 rule in the rubric or sits beside it (this is
   question Q22, still unanswered).
2. **Assessment comes first.** The order is: agree how each skill is
   judged; hand-write treatment 7; only then run the LLM treatments.
   We had it the other way round.
3. **The run of Nov 16 was paused** after 11 calls for separate
   reasons ([archive/model-trials.md](archive/model-trials.md)). It stays paused until
   the assessment sheet is agreed and the split is in.

---

# Further answers, Nov 17-18 2026 (A23, A28, Q25)

Relayed from the class Discord by a team member. Quoted where the
wording matters.

## A28: treatment 7 and the stats

| the note | what it means for us | status |
|---|---|---|
| Treatment 7, the "prudence checks", "is where you learn your expectation of what should be happening. this is a manual modeling task": "build the 20-50 lines of code that links the human task to the (say) EZR code (or whatever else ur comfortable with) to running algorithms." | Per skill, a human writes a small amount of glue (20-50 lines) from the customer's ask to an existing library. Not a from-scratch implementation. | The team's job. Files go in `t7/<domain>/stepNN.py` with the same function contract, so the scorer grades them exactly like T1-T6 (see `t7/README.md`). |
| "The stats tests come later. They are when u compare the results of T1,T2...T7 to see if anyone is performing badly compared to everyone else." | `same` and `ranks` across all seven treatments, per skill. | Built (`rig/report.py`); T7 joins the tables once its files exist. |

## A28: the talk

| the note | what it means for us |
|---|---|
| "review of your progress on the assignment" | A progress report, not a finished result. |
| "tell me things like LOC, token, $$ cost, over the 7 treatments. clock time to run." | A cost table per treatment: new lines, tokens, dollars, wall-clock. `rig/report.py` now prints it. |
| "for the tasks, there is 7 ways of doing everything: where are your stats comparing those 7 ways?" (gloss6) | The per-skill `same`/rank table across T1-T7. |
| "very rough and ready ... < 10 slides. charts. yes. beautiful powerpoint not" | Plain slides, mostly charts. |

## Q25: talks next week are mandatory

12 groups, six per hour, **10 minutes each** including the machine
change, **10 slides at most** ("or even less"). "you will lose marks if
your group does not present. or if you run over time." The lecturer
asked every group to acknowledge the Discord post ("expecting 12
clicks"). **To do: one of us clicks the acknowledgement.**

## A23: runtimes, repeats, and competency

| the note | what it means for us | status |
|---|---|---|
| Runtimes of days are bad: every experiment is run about **6 + 2R** times (fumbling, a first full run, an instrumented run, a fix run, R repeats, then R more after a forgotten measure). | Budget for reruns. One full pass must take minutes to an hour, not days. | Gemini N = 1 took about 45 minutes; Ollama took about 5 hours. |
| "dumb down the model (e.g. Sonnet), reduce data set size (1000 rows, max, picked at random)" | Cap every data set at 1,000 random rows. | Built for prompt v3 runs: `max_rows: 1000` in the configs. HR (1,470 rows) is now capped too. |
| "if you go too dumb on the model then all the results are bad. so you need numbers collected from each run to check for competency" | Every run must report whether the model was competent enough for its results to mean anything. | `rig/report.py` now prints a competency table per treatment (files returned, functions that work, skills that beat the dumb baseline). |
| "you need those competency numbers anyway since you need those to test if one treatment does worse than any other" | Competency feeds the T1-T7 comparison directly. | Same table. |

What A23 does not settle: R itself. The rubric still says N >= 10 for
full marks (open question Q22).
