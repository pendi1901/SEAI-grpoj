# CSC 591 grad project: the whole spec in one place

Source: `txt/seai26f` at commit `5fb51c8` (Mon Nov 16 2026). Every claim
below cites the file it came from. Where the repo is silent or
contradicts itself, that is listed in [open-questions.md](open-questions.md)
rather than guessed.

## 1. What the project is

"The Shrinking-Code Experiment, at Scale" (`docs/submit/gproj.md`). It is
the undergrad project (`docs/submit/uproj.md`) at triple scope:

| | 491 (ugrad) | 591 (us) |
|---|---|---|
| domains | 1 | **3** different clients, 3 different MOOT data sets, **one shared codebase** |
| asks | 20 | 20 **per domain** (60) |
| report | 3 pages | **6 to 9 pages** |
| marks | 25 | **39** = initial 5 + final 34 |
| extra | final exam | **task talk, 15 marks**; no final exam |

Our three domains: software process (`process/pom3a.csv`), open-source
project health (`hpo/Health-*.csv`), HR employee attrition
(`behavior_data/WA_Fn-UseC_-HR-Employee-Attrition.csv`). See
[domains.md](domains.md).

## 2. Dates and marks

| date | what | marks | status on Nov 16 |
|---|---|---:|---|
| Mon Oct 26 | project starts | | |
| Mon Nov 9 | **initial deliverable**: one page + repo | 5 | **already past** |
| Mon Nov 16 or Nov 23 | **task talk**, 20 min (15 + 5 questions) | 15 | this week or next |
| Mon Nov 30 | **final report**, PDF to Moodle, due start of class | 34 | 14 days out |

Late work loses 1 mark per day, weekend counts as one day
(`docs/lect/policies.md`). The project is 39 of the 100 course marks;
with the task talk, 54 marks ride on this work.

### Initial deliverable rubric (5)

| marks | for |
|---:|---|
| 2 | Three requirements docs: twenty customer asks per domain, skill-tagged, **okayed by the lecturer** |
| 2 | One domain's ladder running: tagged steps, tests, one-command demos |
| 1 | The pre-registered claim: both hypotheses and win conditions, verbatim, plus one paragraph on domains and data |

### Task talk rubric (15)

| marks | for | check |
|---:|---|---|
| 3 | The claim: both hypotheses, win conditions, stated first | a stranger could rerun the bet |
| 3 | The evidence: what ran, on what data | treatments and domains named; `same` on every comparison shown |
| 3 | The verdict: results against the claim, honestly | persevere, re-plan or descope, recorded |
| 2 | **Discussed with lecturer the week before** | no discussion = 0 |
| 2 | Timing: done in 15, 5 left for questions | running past 20 = 0 |
| 2 | Slides + delivery | Google Slides, public, **editable by timm@ieee.org**; in person, one presenter, whole group on stage |

Lose marks for: claim stated nowhere or invented after the results;
evidence that cannot be traced to the repo; no time for questions;
slides the lecturer cannot open.

## 3. The two hypotheses (must appear verbatim on page one)

> **The Timm hypothesis.** Neuro-symbolic systems improve when
> their symbolic half is factored into small reusable structures.
> The ten skills are synonyms: one
> machine (cluster, tree, leaf) wearing ten hats. Hence an LLM, or
> a human, extends a well-factored library with less new code, and
> fewer errors, than a monolithic one.

> **The rival.** The ten skills are ten separate problems. Factoring
> buys nothing: skill i+1 costs about the same whoever writes it,
> and whatever library sits underneath.

Falsifiable prediction: the shape of the new-code histogram. Bars fall
= reuse is real. Bars flat = the rival wins. Either result scores.

**Pre-registration** (gproj.md): both hypotheses and their win
conditions are written down *before* coding. Metric: new code per step
and `same`-certified wins. Baseline: the no-reuse treatments. The final
report delivers a verdict against that written claim. Paraphrasing or
stating one side only earns half the Hypotheses marks.

## 4. The ten skills

Every ask in a requirements doc is tagged with one of these
(uproj.md car-yard table; core names from `docs/gloss10.md`):

| # | skill | plain meaning | core form |
|--:|---|---|---|
| 1 | remember | find the unusually good rows | retrieval |
| 2 | guess | predict a goal before measuring it | regression |
| 3 | certify | is this difference real or noise | `same()` |
| 4 | flow | decide as rows arrive one at a time | `disty`, streamed |
| 5 | blame | say why the bad rows are bad | explanation |
| 6 | justify | defend a verdict to a skeptic | `disty` percentile + explanation |
| 7 | choose | find the best row with few labels | optimization |
| 8 | fix | cheapest change that repairs a bad row | planning |
| 9 | spot | find the typo or the scam | anomaly |
| 10 | race | our method against the field | benchmarking |

Reference cost curve (auto93, in Lua): 150, 57, 40, 27, 20, 13, 10, 10,
6, 0 new lines, 333 in all. Skill 1 costs 45% because it pays for the
shared data structures.

## 5. The four moves

1. **Pick a domain** MOOT data supports.
2. **Write a requirements doc** at `docs/requirements.md`: twenty asks,
   one line each, in the client's words, never algorithm words ("find me
   a great car cheap", not "run NSGA-II"). Tag each with its skill.
   Written before coding. Honest work for the client, not twenty
   restatements of one query. **Get it okayed by the lecturer.** Going
   from ten to twenty is "the interview": keep asking for trends,
   alerts, forecasts, what-ifs and why-nots until worries stop
   repeating.
3. **Build the skills in steps**, each step git-tagged `step1`,
   `step2`, ... Each step should reuse the earlier ones, so step i+1
   needs less new code than step i. The tag history is marked.
4. **Hand in** the report.

For 591, by the third domain "you should be writing almost nothing
except the wish list".

## 6. The experiment: seven treatments

| # | who writes skill i+1 | background code | told to reuse skills 1..i? |
|--:|---|---|:--:|
| 1 | LLM | plain Python | no |
| 2 | LLM | plain Python | yes |
| 3 | LLM | scikit-learn | no |
| 4 | LLM | scikit-learn | yes |
| 5 | LLM | ezr | no |
| 6 | LLM | ezr | yes |
| 7 | **you** | your own prior skills | reuse as much as you can |

**Treatment 7 is the human part.** It is the seventh *treatment*, not a
seventh task: a team member writes every skill by hand, trying as hard
as possible to reuse, and it is the control the six LLM treatments are
compared against.

Lecturer's ruling (Discord A21, Nov 16): **one handwritten run of all
ten skills** per data set is enough; no repeats. An LLM may be used as
a search tool or tutor ("where is the stuff relating to xxxx", "write
me a tutorial with examples on how to use a decision tree"). "LLM auto
assembly (please build me that bit) is out of court."

Same game in every treatment: to get skill i+1, supply the background
library, the code for skills 1..i, and the one-line requirement. Then
measure (a) how much new code appears and (b) how well the result runs.

Treatments 1, 3, 5 are the rival's day in court: one fresh prompt per
skill, no instruction to reuse.

## 7. Repeats and the reset rule

Run the whole thing N times.

| N | verdict | Results marks (of 9) |
|--:|---|---|
| 20 | "the dream" | full |
| 10 | "earns congratulations" | full (N >= 10) |
| 3 | "the floor below which there are no statistics, only anecdotes" | half |

Each trial must face an LLM that remembers nothing:

- one-shot headless calls (`claude -p`, or the API with empty history);
- memory features off;
- **no CLAUDE.md**;
- one fresh directory per trial;
- a new chat window is **not** enough if memory or project context is on.

Trials that shared a context are one trial, counted once, and cap
Methods at 1 mark of 5.

## 8. Statistics

Report a difference only when `same` says there is one. Claims without
`same` score **0 of 9** on Results. Details, plus the per-skill Q score
and the Z rescaling from gloss10, are in [stats.md](stats.md).

## 9. When ezr loses

Expected on the first pass: ezr is untuned for our data. Fixing it is
part of the project and goes in Methods.

- **(a) Wire up the oracle.** `TBL:label` in `ezr.lua` (line 291) asks
  `i.model` for the goals of a row whose goals are `?`. Change it so an
  unseen row actually runs something we control.
- **(b) Tune ezr with ezr.** Build a MOOT-style csv: each row a random
  pick of the low-level controls `few`, `p`, `keepf`, `leaf`, `maxd`,
  `more`, `stop` (**not** the meta controls `budget` and `check`), goal
  columns scoring how well that pick did. Point ezr at it.

Defaults today: budget=50, check=5, few=128, keepf=0.66, leaf=3,
maxd=4, more=4, p=2, stop=32. If tuned ezr still loses, say so.

## 10. The report

LaTeX `acmart`, ACM transactions format, **6 to 9 pages**, one PDF to
Moodle, **repo URL on page one**. Over the page limit loses marks. Five
section headers, in this order:

1. **Hypotheses.** Both, verbatim, then one paragraph: domains, data,
   and what result makes each side win.
2. **Requirements.** Twenty asks per domain, each skill-tagged.
3. **Methods.** Seven treatments, the reset protocol actually used, N,
   any ezr tuning.
4. **Results.** Histograms (x = step, y = % new code, from git tags via
   `git diff --stat step2..step3` or cloc per tag, one line per
   treatment) and the `same` tables. 591 adds transfer evidence across
   domains.
5. **Discussion.** Which hypothesis won, where, and why, using only
   differences `same` certifies. Per domain and overall.

The repo must be: public; steps tagged; tests present;
`docs/requirements.md`; a README that runs every demo in one command
each; shared across the three domains.

## 11. Final rubric (591 column, 34 marks)

| marks | section | for | 3-point check |
|---:|---|---|---|
| 3 | Hypotheses | both claims, win conditions named | verbatim + win conditions = full; paraphrased or one-sided = half |
| 7 | Requirements | 20 asks x 3 domains, customer words, skill-tagged | all = full; two-thirds = half; algorithm words = 1 |
| 5 | Methods | seven treatments, documented resets, N declared | all three = full; shared contexts = 1 |
| 9 | Results | histograms derivable from tags, `same` on every comparison, transfer evidence | N>=10 = full; N=3 = half; claims without `same` = 0 |
| 4 | Discussion | verdict follows from tables, per domain and overall | unsupported conclusions = 0 |
| 3 | The repo | tags, tests, one-command demos, shared across domains | a demo that only "ran once" = 0 |
| 3 | AI disclosure | what the LLM wrote, which of its errors we caught | zero caught errors reads as zero checking |

## 12. Every listed way to lose marks

From uproj.md:

- a histogram not derivable from the repo's tags;
- steps that share nothing (nine little programs is not a ladder);
- code dumped in one final commit;
- requirements written in algorithm words;
- trials that shared an LLM context;
- a "difference" that `same` calls noise;
- a report over the page limit.

Added for 591 (gproj.md):

- three domains that are one domain wearing three hats;
- a third domain with no transfer numbers (how much old machinery did
  it reuse?);
- a verdict that quietly drops one of the three domains.

## 13. Doctrine that shapes the marking

- **Failures are findings.** A domain that "laughs at you", honestly
  diagnosed, scores. A hidden failure does not. A failed claim with a
  recorded decision loses nothing.
- **Say what it cost.** "A score without its label count, or without
  saying pure-vs-generalize, is not a result" (gloss10).
- **Ties are the normal case.** Rank 0 is a set, not a name. Naming one
  winner when four tie is "the most common statistical lie in this
  field" (gloss6).
- **Judge more than accuracy.** A preliminary grad result quoted in
  `docs/review/w8.md`: systems scored about the same; code size,
  runtime, construction effort and maintainability (tokens needed to
  maintain) differed wildly.
- **AI use is allowed and must be disclosed**; we must be able to
  explain everything we submit (policies.md).
