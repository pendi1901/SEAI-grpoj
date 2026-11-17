# Requirements: forecasting open-source project health

**Status: DRAFT.** First draft written by an LLM (Claude) on Nov 16
2026. Not yet edited by the team. Not yet okayed by the lecturer.

## The client

An analyst in a company's open-source office. The company depends on
outside projects and wants a year's warning before one goes quiet. He
runs a forecasting tool that predicts how many issues a project will
close in the next twelve months. The tool has five settings. A bad
choice of settings gives forecasts nobody can trust, and every setup he
tries costs a full run.

His problem is the tool's setup, not the projects themselves. The data
cannot say which projects are dying; it says which setups forecast
well.

## The data

`moot/optimize/hpo/Health-ClosedIssues0000.csv` (proposed): 10,000
setups of the forecasting tool, each scored on one GitHub project.
Five settings per setup, three results.

| column | in his words |
|---|---|
| N_estimators | how big the forecaster is (bigger takes longer to run) |
| criterion | which of the tool's built-in rules it uses to judge its own guesses |
| Min_sample_leaves | how few past cases it will base a guess on |
| Min_impurity_decrease | how much better a refinement must be before it bothers |
| Max_depth | how many questions deep it may go |
| MRE- | how far off the forecasts were, on average (lower is better) |
| ACC+ | the tool's accuracy score (higher is better) |
| PRED40+ | share of forecasts that landed within 40% of the truth (higher is better) |

To confirm before coding:

- Which file. There are 35 (`ClosedIssues`, `ClosedPRs`, `Commits`,
  about 12 projects each). Some are useless: in `ClosedPRs0000` every
  setup scores one of two values. `ClosedIssues0000` has real spread
  on MRE and ACC, but PRED40 is 0 for most rows.
- The other files are the same question on other projects, so they
  can serve ask 20.

**What he can change (proposed):** all five settings.
**Standing limit:** run time. A fix may not make the forecaster
bigger than it is now.

## The twenty asks

| # | he asks | skill |
|--:|---|---|
| 1 | Out of the 10,000 setups already tried, show me the handful whose forecasts were unusually trustworthy. | remember |
| 2 | Before I spend an hour running a setup, tell me roughly how far off its forecasts will be. | guess |
| 3 | In my last batch the big setups looked more accurate than the small ones. Is that real, or noise? | certify |
| 4 | Results come back from the build farm one setup at a time. Tell me the moment I have seen one good enough to ship; I will not rerun the others. | flow |
| 5 | Why do the bad setups miss so badly? Which settings are doing the damage? | blame |
| 6 | You say this setup is good. How good, against all the others, and why should I believe it? | justify |
| 7 | I have time to try 50 setups. Find me the best one. | choose |
| 8 | The setup we use today forecasts poorly. What is the smallest change to its settings that makes it acceptable, without making it slower? | fix |
| 9 | Some result rows look like a run that failed and got written down anyway. Find them. | spot |
| 10 | Three colleagues have three ways of hunting for a good setup. Give each the same 50 runs. Who wins? | race |
| 11 | Here is the setup the team uses today. Show me the tried setups most like it, and how they scored. | remember |
| 12 | If I halve the size of the forecaster to save run time, how much worse do the forecasts get? | guess |
| 13 | Does the choice between the tool's two built-in rules make any real difference, or can I stop arguing about it? | certify |
| 14 | Results arrive every night. Tell me when the best so far has stopped improving, so I can stop paying for runs. | flow |
| 15 | Which settings can I leave at the factory default without hurting anything? | blame |
| 16 | Why not simply use the biggest, deepest setup the machine can hold? | justify |
| 17 | Find me a setup that forecasts well and is also small enough to run every night. | choose |
| 18 | Fix my setup, but I am only allowed to change one setting. | fix |
| 19 | A colleague suggests settings far outside anything we have tried. Tell me when you are being asked about something you have never seen. | spot |
| 20 | The setup you picked for this project: on a different project's results, does it still beat picking at random? | race |

Each skill appears twice. Asks 1 to 10 are the first interview. Asks
11 to 20 came from asking for look-alikes, what-ifs, stopping rules,
why-nots and limits until the worries started to repeat.

## A warning for the report

This is the domain most likely to show nothing. Five settings, a
result column that is mostly zero, and some files with no spread at
all. If a skill has nothing to learn here, that is a result to report,
not a reason to swap the data set quietly.
