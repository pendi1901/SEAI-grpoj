# The three domains

**Since Nov 18 every run uses 1,000 rows per data set, picked at random
with a fixed seed, then split 800 training / 200 test** (lecturer's A23).
The full sizes below describe the source files.

Data: `github.com/timm/moot`, `optimize/`. Header convention: a name
starting in upper case is numeric, lower case is symbolic; a trailing
`-` is a goal to minimise, `+` to maximise; everything else is an x
column. Facts below were measured from the files on Nov 16 2026.

| | software process | project health | HR attrition |
|---|---|---|---|
| file | `process/pom3a.csv` | `hpo/Health-*.csv` (35 files) | `behavior_data/WA_Fn-UseC_-HR-Employee-Attrition.csv` |
| rows | 20,000 | 10,000 each | 1,470 |
| x columns | 9, all numeric | 5 (4 numeric, 1 symbolic) | 32, mixed |
| goals | `Cost-` `Score-` `Idle-` | `MRE-` `ACC+` `PRED40+` | `YearsAtCompany+` `YearsInCurrentRole+` `YearsWithCurrManager+` |
| origin | simulator output | hyperparameter sweep | the IBM HR Analytics sample, widely described as fictional data built by IBM; confirm before calling it real |
| named in uproj.md | yes | yes | no, but it is in MOOT |

The three differ in kind (a simulation, a tuning log, people records),
which is the defence against "one domain wearing three hats".

## 1. Software process: pom3a

POM3 simulates the Boehm and Turner model of agile development: the
trade between idle rates, completion rates and cost. Teams go idle
waiting on other teams; hiring fixes that and raises cost. pom3a is the
simplest of four (a < b < c < d).

x: Culture, Criticality, Criticality Modifier, Initial Known,
Inter-Dependency, Dynamism, Size, Plan, Team Size. All scaled 0..1.

Client: someone setting up an agile programme (a delivery manager).

Watch for:

- **Every x value is unique** (20,000 distinct per column). It is a
  random sample of a continuous space, so there are no natural groups
  and no repeated rows.
- 20,000 rows makes any all-pairs code slow. Sample or cap.
- x columns are abstract simulator knobs. Customer-word asks need a
  plain-language reading of each ("how much of the work we knew up
  front", not "Initial Known").
- `Score-` is minimised in the header; check what it means before
  writing an ask about it.
- Levers for the fix skill: Plan, Team Size and perhaps Culture are
  choices; Criticality, Size, Dynamism are facts about the project.

## 2. Open-source project health: Health-*

Each row is one random-forest configuration; the goals say how well
that forest predicted a GitHub project's activity 12 months ahead.
Three families: `ClosedIssues` (12 files), `ClosedPRs` (11 files, no
0001), `Commits` (12 files). Each numbered file is a different project.

x: N_estimators, criterion, Min_sample_leaves, Min_impurity_decrease,
Max_depth.

Watch for:

- **The rows are tuner configurations, not projects.** The honest
  client is an analyst who must forecast project health and wants to
  know how to set up the forecaster cheaply. A wish list about "which
  repos are dying" is not what this table can answer.
- **Some files are degenerate.** `Health-ClosedPRs0000`: MRE takes only
  2 values, PRED40 only 2, median MRE 0 and median PRED40 1; it has no
  ACC column. Nothing to learn there. `ClosedIssues0000` and
  `Commits0000` have real spread on MRE and ACC, but PRED40 has only
  6 to 8 distinct values with median 0.
- Only 5 x columns: explanations will be short, and "spot" has little
  room to hide an anomaly.
- Pick one file as the domain's data set and say which. The other 34
  are a ready-made transfer or robustness check.
- This is the domain most likely to "laugh at us". That scores if
  diagnosed.

## 3. HR employee attrition

1,470 employees: demographics, job, pay, satisfaction, history.

Watch for:

- **`attrition` is an x column, not a goal.** It is lower-case, so
  symbolic, with no `+`/`-`. The goals are three tenure measures. So
  the table optimises "long tenure", and attrition is one feature among
  32. Asks like "who is about to quit?" must be phrased against what
  the data scores, or the mismatch must be stated.
- The three goals are near-duplicates of each other (all tenure) and
  are correlated with x columns such as TotalWorkingYears and Age.
  Good guess scores here may be leakage-flavoured rather than insight.
- **Dead columns:** `EmployeeCount` (always 1), `over18` (always Y),
  `StandardHours` (always 80). `EmployeeNumber` is a row id (1,470
  distinct). A clustering that uses the id is wrong; a good "spot" or
  "blame" should never name these.
- Small table: 30 train/test splits are cheap, but 5% of rows for
  "remember" is only 73.
- Levers for fix: overtime, business travel, training, salary hike,
  stock options. Not levers: age, gender, marital status. Writing a fix
  that changes a protected attribute is a finding worth a sentence.
- It is data about people, synthetic or not. Keep the client's asks
  about policy, not about individuals.

## What transfer evidence looks like

gproj.md asks "how much old machinery did it reuse?" for the third
domain. Per domain, in the order built:

- lines of shared code used unchanged, lines changed, lines new;
- the same as a percentage of that domain's total;
- which skills needed domain-specific code, and why.

If the hypothesis holds, domain 3 is close to a wish list, a header
row and a lever list.
