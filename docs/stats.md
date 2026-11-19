# Statistics: what to compute, and when

Sources: `docs/gloss6.md` (week 6, diagrams added Nov 16),
`docs/gloss10.md` (the Nov 16 lecture page), `src/ezr-lua/ezr.lua`
lines 617-680, `docs/submit/uproj.md`.

There are three layers. Only the first is written into the rubric. The
second and third come from gloss10.

## Layer 1: `same`, on every comparison (rubric, mandatory)

Two treatments never print identical numbers. `same` decides whether
the gap is real. It is three tests, and two samples are the same only
when **all three** agree:

| test | question | formula | "same" when |
|---|---|---|---|
| `cohen` | how big is the mean gap? | abs(mu_x - mu_y) / pooled sd | <= 0.35 |
| `cliffs` | of all (x,y) pairs, how lopsided is x>y vs x<y? | abs(gt - lt) / (n_x * n_y) | <= 0.195 |
| `ks` | how far apart are the two cdfs? | max cdf gap / sqrt((n_x+n_y)/(n_x*n_y)) | <= 1.36 |

```lua
function same(xsort,ysort,Cohen,Ks,Cliffs)
  return cohen( xsort,ysort) <= (Cohen  or .35)
     and cliffs(xsort,ysort) <= (Cliffs or .195)
     and ks(    xsort,ysort) <= (Ks     or 1.36) end
```

Things that will bite:

- **Inputs must be sorted.** `cliffs` and `ks` walk both lists in order.
- Cohen is an effect size, not a p-value. It asks "how big", not "how
  surprising".
- KS at 1.36 is the 5% line, so it cries wolf about one time in twenty
  on identical generators. That is why one test never decides alone.
- The course repo has `same` only in Lua. The lecturer's stats link
  (Discord, Nov 16) is the Python one: next section.

### The Python `same` (the lecturer's link)

`github.com/timm/ezr/blob/main/ezr.py`, section `#-- stats --`. The
link given was `#L320-L359`; the file has moved since, and on Nov 16
the stats sit at lines 325-364. Pin a commit hash when citing it.

```python
def same(xs, ys, eps=0):
  xs, ys = sorted(xs), sorted(ys)
  return (cliffs(xs,ys) and ks(xs,ys)
          and (not eps or cohen(xs,ys,d=eps)))
```

It is not identical to the Lua version. State which one the report
uses:

| | Lua `ezr.lua` (course repo) | Python `ezr.py` (the link) |
|---|---|---|
| tests run by default | cohen, cliffs, ks | **cliffs and ks only** |
| cohen | always, at 0.35 | only if `eps` is passed; `eps` is its threshold |
| cliffs threshold | 0.195 | 0.197 |
| ks threshold | 1.36 | 1.36 |
| sorts its inputs | no, caller must | yes |
| each test returns | a number | a boolean |
| `ranks` | yes | **no**; write the median-sort-and-walk ourselves |

To match the three-test rule in gloss6, call `same(xs, ys, eps=0.35)`.

### `ranks`: the table the paper prints

Sort treatments by median. Walk down. A treatment gets a new rank only
when it is not `same` as the current rank's leader. So ties share a
rank and rank 0 is a **set**. `ranks(d, big)`: pass `big=true` when
higher is better (Q is higher-is-better; new lines of code is
lower-is-better).

A `same` table is therefore: one row per treatment, median, spread, and
rank, for one measure in one domain at one step (or over all steps).

### What gets compared

Each (domain, treatment, step) cell holds N numbers, one per trial.
With seven treatments that is one `ranks` call per (domain, step,
measure). The two measures the spec names:

1. **new code** for that step (lines added; from tags);
2. **how well the result runs** (the Q below).

N = 3 gives `same` three numbers per side. That is why the spec calls
3 "anecdotes" and halves the Results marks.

## Layer 2: Q, a score per skill (gloss10)

gloss10 scores each skill with a protocol and a number Q, higher is
better. "Score" inside the table means `disty`, the domain's combined
objective, lower is better.

| skill | what the scorer does | Q | baseline |
|---|---|---|---|
| 1 remember | skill returns up to 5% of rows it judges best | 1 - (median score of returned rows / median score of random sets of the same size) | 0 |
| 2 guess | 30 train/test splits; predict the target on held-out rows | mean of 1 - (error / error of predicting the training average) | 0 |
| 3 certify | 200 sample pairs: half the same, half shifted 0.5, 1 or 2 sd; three shapes; sizes 10, 30, 100 | balanced accuracy of "same" vs "different" | 0.5 |
| 4 flow | 100 random arrival orders; commit the moment a row is read | mean of 1 - (chosen row's score / mean score of the stream) | 0 |
| 5 blame | names columns and rules explaining a poor score | rewrite blamed cells to values no row blames, re-score: (old - new) / old, **minus** the same delta from rewriting as many random columns | 0 |
| 6 justify | 20 rows from the best quarter; returns a score percentile and a text reason | (error of answering 0.5 - error of the answer) / error of 0.5 | 0 |
| 7 choose | 30 runs; at most 50 labels; return the best row found | win rate vs the best of 50 random rows: win 1, tie 0.5, loss 0 | 0.5 |
| 8 fix | 20 worst-quartile rows; return a change to allowed lever columns only | share of the 20 with a valid change (levers only, values in range). **Does not measure improvement.** | |
| 9 spot | 30 copies of 1,000 rows with 10 injected errors | precision at 20 | about 0.01 |
| 10 race | 30 runs; race >= 3 strategies, one random, within 50 labels | win rate of the returned winner vs random-50; invalid race = failed | 0.5 |

The last column is the gloss10 "dumb" level. What a *failed* program
earns differs for choose: 0, not 0.5 (decision A in
[assessment.md](assessment.md)), so that a crash never outscores a weak
working answer. Both values live in `rig/contract.py` (`BASELINE` is the
failure value, `DUMB` the no-effort level).

The three moves behind every Q:

1. pick a dumb rival that costs nothing (random rows, the training
   average, chance, always 0.5);
2. scale against it so 0 (or 0.5) means "no better than dumb";
3. **score failures at the baseline.** "A call that fails earns the
   baseline value in the primary analysis: crashing is not a way to sit
   out a round."

Per-domain facts the scorer needs that we must write down first: which
columns are **levers** for skill 8 (a manager can change team size, not
project criticality), and how errors are injected for skill 9.

## Layer 3: Z, before comparing across skills or domains (gloss10)

Each skill has its own scale and baseline (0 for some, 0.5 for others,
0.01 for spot), so raw Q cannot be averaged or compared. "Before
comparing conditions, the analysis re-expresses Q as Z within each
domain and skill."

Reading: for one (domain, skill), pool the Q values from every
treatment and trial, take mean and sd, and replace each Q with
(Q - mean) / sd. Then treatments can be compared across skills and
domains on one axis. The page gives no formula beyond that sentence, so
the pooling choice is ours to state in Methods.

## What to log after every run

One row per LLM call (or per hand-written step), appended to a csv the
moment the call ends. Nothing in the analysis should need a re-run.

| field | why |
|---|---|
| domain, data file | three domains, never dropped silently |
| treatment 1-7 | the comparison |
| trial 1..N, seed | repeats; reproducibility |
| step / skill | x-axis of the histogram |
| fresh dir path, command line, model id | proof of the reset protocol (Methods, 5 marks) |
| new lines, total lines, % new | the histogram; must match what the tags give |
| ran? (exit status), tests passed | failures are scored at baseline, not dropped |
| Q | how well it runs |
| labels spent | "a score without its label count is not a result" |
| wall seconds, tokens in/out | cost; the w8 note says judge on these too |
| errors we caught in the LLM's code | AI disclosure, 3 marks; zero caught = zero checking |

After every **step** (all treatments, all trials in): one `ranks` table
per measure. After every **domain**: the histogram, the Z-scaled
comparison, and the transfer number (how much of the previous domain's
code was reused unchanged).
