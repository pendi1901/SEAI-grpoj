# Requirements

**Status: DRAFT.** Written by an LLM (Claude) on Nov 16 2026 from the
course spec and the data files. The team has not edited these yet and
the lecturer has not okayed them. Both must happen before they count.

Three clients, three data sets, twenty asks each, every ask tagged
with the skill it will demo.

| domain | client | data | asks |
|---|---|---|---|
| software process | head of delivery setting up agile programmes | `process/pom3a.csv` | [requirements/process.md](requirements/process.md) |
| project health | analyst setting up a tool that forecasts project activity | `hpo/Health-ClosedIssues0000.csv` (proposed) | [requirements/health.md](requirements/health.md) |
| staff retention | head of people who wants staff to stay longer | `behavior_data/WA_Fn-UseC_-HR-Employee-Attrition.csv` | [requirements/hr.md](requirements/hr.md) |

## Why these are three domains, not one in three hats

| | process | health | retention |
|---|---|---|---|
| a row is | a simulated programme | one setup of a forecasting tool | a person |
| the client changes | planning and staffing | tool settings | working arrangements and rewards |
| the client cannot change | facts about the project | nothing, but run time is capped | who the person is |
| size | 20,000 rows, 9 facts | 10,000 rows, 5 facts | 1,470 rows, 32 facts |
| facts are | all numbers | numbers and one category | numbers and categories mixed |

## Skill coverage

Every skill is asked for twice in every domain: 6 asks per skill, 60
in all.

| skill | process | health | retention |
|---|---|---|---|
| remember | 1, 11 | 1, 11 | 1, 11 |
| guess | 2, 12 | 2, 12 | 2, 12 |
| certify | 3, 13 | 3, 13 | 3, 13 |
| flow | 4, 14 | 4, 14 | 4, 14 |
| blame | 5, 15 | 5, 15 | 5, 15 |
| justify | 6, 16 | 6, 16 | 6, 16 |
| choose | 7, 17 | 7, 17 | 7, 17 |
| fix | 8, 18 | 8, 18 | 8, 18 |
| spot | 9, 19 | 9, 19 | 9, 19 |
| race | 10, 20 | 10, 20 | 10, 20 |

## For the team to decide before sending to the lecturer

1. **Which Health file.** `ClosedIssues0000` is a proposal. Check a
   few others for spread first.
2. **The lever lists** in each file ("what the client can change").
   They drive the fix skill and are proposals.
3. **The retention goal.** The data scores length of stay; `attrition`
   is an input. The asks are written about staying. Say so to the
   lecturer rather than let him find it.
4. **The pom3a column readings**, and what `Score-` means.
5. **Rewrite in your own voice.** These asks should sound like a
   client you can defend in the talk. Change any that do not.
6. **Disclose** in the report that the first draft was LLM-written and
   what you changed.
