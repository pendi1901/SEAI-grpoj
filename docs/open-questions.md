# Open questions

Updated Nov 18 2026. Lecturer answers so far are in
[lecturer-notes.md](lecturer-notes.md) (Nov 16 notes, A21, A23, A28,
Q25). Ask the rest at an appointment this week.

## For the lecturer

1. **Q22: is N = 1 enough?** The rubric gives full Results marks only
   for N >= 10 and half for N = 3. A23 describes "R repeats" without a
   number, and his Nov 16 notes call one domain and one repeat an
   accepted fallback, with test rows supplying the numbers. Does one
   repeat, compared on per-test-case numbers, earn full marks?
2. **The repair round.** Prompt v3 gives each LLM treatment one retry
   with the error from running its function on training data. Is that
   acceptable as part of the treatment?
3. **Our scorer.** gloss10 gives one line per skill and no code. We
   wrote `rig/score.py` to that table, with the departures listed in
   `docs/assessment.md`. Is there an official scorer we should use?
4. **Ten steps.** We use asks 1 to 10, one per skill (A21 says "all ten
   skills"). The other ten asks per domain are in the requirements but
   not run. Fine?
5. **No-reuse treatments see the earlier code.** uproj.md says to supply
   "the code for skills 1..i" in every treatment; T1, T3 and T5 see it
   but are not told to reuse it. Is that the intended reading?
6. **Tags for the LLM ladders.** "Histograms derivable from the repo's
   tags" fits one hand-built ladder (T7, tagged per step). For T1 to T6
   we store every step's file per trial and derive the histogram from
   those. Acceptable?
7. **The HR goals.** The table's goals are tenure; `attrition` is an
   input. Our HR asks are about staying longer. OK?
8. **Which Health file.** We use `Health-ClosedIssues0000`. Fine as one
   of three domains?

## Only the team knows

- Was the Nov 9 initial deliverable handed in? It needed the three
  requirements docs **okayed by the lecturer** and the pre-registered
  claim. The drafts here say "not yet okayed".
- Is there a pre-registered claim written before coding, with a date?
  If not, write it now, date it honestly, and say so in the report.
- Has the lecturer seen the talk plan? (2 marks, all or nothing.)
- Who clicked the Discord acknowledgement for the talks?

## Settled

| question | answer | source |
|---|---|---|
| How many hand-written runs for T7? | one, all ten skills | A21 |
| May T7 use an LLM? | as a search tool or tutor only; no generated code | A21 |
| What is T7? | 20 to 50 lines of glue per skill from the ask to EZR or a library | A28 |
| Which stats? | `same` across T1-T7 (lecturer's Python `ezr.py`) | Nov 16 notes, A28 |
| Train/test? | 80/20, one test suite for every treatment | Nov 16 notes |
| Data size? | at most 1,000 random rows | A23 |
| Budget? | about $100 a person; cheaper models encouraged | Nov 16 notes |
| How to assess each skill? | `docs/assessment.md`, signed off Nov 17 | Nov 16 notes |
| Talks? | mandatory, next week, 10 minutes, at most 10 slides | Q25 |
