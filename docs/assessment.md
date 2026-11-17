# How each skill is assessed: read, argue, sign off

The lecturer's instruction (Nov 16): "work thu each task and ask the LLM
how would we assess this one? see if you agree with its methods. dont go
on until you do."

This sheet is the LLM's answer (Claude, Nov 16 2026). It is a proposal.
**No large run starts until a human on the team has read every row
below and ticked it or changed it.** Where I had a doubt, it is written
down as a question for you.

## The set-up, the same for every skill

1. **Split each data set once, 80/20, with a fixed seed.** The 80% is
   the training set. The 20% is the test suite.
2. **A treatment only ever sees the training set.** That is the file
   in its directory and the rows shown in its prompt.
3. **Every treatment and every trial is tested on the same test
   suite**, with the same test cases, built once per domain and skill.
4. **Each skill is a function.** The prompt tells the LLM its name
   and arguments; the scorer imports the file and calls it.
5. **Each test case gives one number**, scaled so that a no-effort
   answer earns the "dumb" value in the table. A treatment's score for
   a skill, Q, is the mean over its test cases.
6. **A failure earns the dumb value on every test case.** A missing
   function, a crash, a hang (5 minutes) or an answer outside the
   rules all count. Crashing is not a way to sit out.
7. **Treatments are compared with `same`** on those lists of
   per-test-case numbers: one list per treatment, for each skill in
   each domain.

"Score" below means how far a row's goals are from the best possible,
from 0 (best) to 1 (worst), each goal scaled by its range in the
training set.

## The ten skills

| # | skill | the customer wants | the function is given | one test case is | its number (higher is better) | dumb earns | agree? |
|--:|---|---|---|---|---|--:|:--:|
| 1 | remember | a short list of unusually good rows | the test rows | one row it returned (it may return up to 5% of them) | 1 - that row's score / the median score of a random list of the same length | 0 | [ ] |
| 2 | guess | an estimate of a goal before measuring | training rows; test rows with goals hidden | one test row | 1 - its error on that row / the average error of always guessing the training mean | 0 | [ ] |
| 3 | certify | "is this difference real or noise?" | two lists of numbers | one pair of lists: 200 pairs, half identical in origin, half shifted by 0.5, 1 or 2 standard deviations; three shapes; sizes 10, 30, 100 | 1 if it said "same" or "different" correctly, else 0 | 0.5 | [ ] |
| 4 | flow | a decision on each row as it arrives, no going back | the arriving row, and the rows seen before it | one arrival order of 100 test rows (100 orders) | 1 - the score of the row it stopped on / the average score in the stream | 0 | [ ] |
| 5 | blame | which inputs make the bad rows bad | the training rows | one of 30 test rows from the worst quarter | drop in that row's estimated score when the blamed columns are reset to typical good values, minus the drop from resetting as many random columns | 0 | [ ] |
| 6 | justify | "how good is this one, and why?" | training rows; one test row with goals hidden | one of 20 test rows from the best quarter | how much closer its percentile is than always answering "50th"; a reason in words is required | 0 | [ ] |
| 7 | choose | the best row, measuring very few | 150 test rows with goals hidden; a `label` function it may call on 50 rows | one run on a fresh draw of rows (30 runs) | 1 win, 0.5 tie, 0 loss against the best of 50 rows picked at random | 0.5 | [ ] |
| 8 | fix | a change that could rescue a bad row | one bad test row; the columns it may change and their allowed values | one of 20 test rows from the worst quarter | 1 if the change uses only allowed columns and values and changes something, else 0 | 0 | [ ] |
| 9 | spot | the entries that look wrong | test rows, 10 of which had one input replaced by a value 6 standard deviations out | one corrupted copy (10 copies) | hits among its first 20 suspects, divided by 20 | 0 | [ ] |
| 10 | race | which search strategy wins on the same budget | as for choose | one run (30 runs) | as for choose, for the row its winning strategy found; 0 if fewer than three strategies, no "random" strategy, or more than 50 labels | 0 | [ ] |

## Doubts I want you to rule on

1. **Fix does not check that the change helps.** gloss10 says so
   itself: "It does not measure improvement." A treatment that always
   flips one lever scores 1. Keep it as the course defines it, or add
   a second number (estimated improvement after the change)?
2. **Blame has no ground truth.** On real data nobody knows the true
   effect of changing a column. I estimate a rewritten row's score
   from its 5 nearest training rows. That is a model judging a model.
   Acceptable, or should blame be judged only on the simulator-backed
   domain (pom3a)?
3. **Spot can score at most 0.5**, because only 10 errors are planted
   and it is judged on its first 20. That is gloss10's rule. Fine, or
   judge the first 10 instead?
4. **Spot's errors are crude.** A value 6 standard deviations out is
   easy to find. Real typos are subtler. Easier errors make all
   treatments look alike near the top.
5. **Remember sees the goals.** It is retrieval, so the function gets
   complete rows and sorting by goals is a legitimate answer. That
   makes skill 1 nearly free to pass, which also makes it a weak test.
6. **Justify's "reason" is not graded**, only required. Grading text
   needs a human or another LLM. Leave ungraded?
7. **Choose and race report 0.5 for a failure** but a skill that
   picks one row at random scores about 0, because it loses to the
   best of 50. So failing beats trying badly. That is gloss10's rule
   ("chance = 0.5"). Keep, or set failure to 0?
8. **The HR goals.** All three goals are tenure, and tenure tracks
   age and total working years, which are inputs. Guess will look
   strong here for a boring reason.
9. **One fixed split.** Results depend on which 20% was drawn. A
   single split is what the lecturer described; it could be repeated
   with a few seeds later if time allows.
10. **Levers** (what each client may change) are my proposals in
    `rig/config.json`. Fix is scored against them.

## What "agree" commits you to

Whatever is ticked here is what Methods must describe and what the
talk must defend. If you change a row after runs have started, the
runs before and after are not comparable and the earlier ones must be
rescored or dropped. Rescoring is cheap (minutes, CPU only); rerunning
the LLM is not needed, because every generated program is kept.

Signed off by: ____________  Date: ____________
