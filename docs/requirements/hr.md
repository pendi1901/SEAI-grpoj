# Requirements: keeping staff longer

**Status: DRAFT.** First draft written by an LLM (Claude) on Nov 16
2026. Not yet edited by the team. Not yet okayed by the lecturer.

## The client

The head of people at a company of about 1,500 staff. Replacing
someone who leaves costs her months of salary. She wants people to
stay longer: with the company, in their role, and with their manager.
She controls working arrangements and rewards. She does not control,
and must not act on, who people are.

## The data

`moot/optimize/behavior_data/WA_Fn-UseC_-HR-Employee-Attrition.csv`:
1,470 staff records, 32 facts each, three results.

| results | in her words |
|---|---|
| YearsAtCompany+ | how long they have stayed with us (higher is better) |
| YearsInCurrentRole+ | how long they have stayed in their role |
| YearsWithCurrManager+ | how long they have stayed with their manager |

The 32 facts cover: age, gender, marital status, education;
department, job role and level; pay, pay rise, stock options;
overtime, business travel, distance from home, training; four
satisfaction ratings; work history.

To confirm before coding:

- **The data scores length of stay, not leaving.** The column
  `attrition` (did they leave: yes or no) is one of the 32 facts, not
  a result. So every ask below is about staying longer. If the team
  wants "who is about to quit" as the question, that needs the
  lecturer's agreement, because the table is not set up to score it.
- The three results measure nearly the same thing, and are tied to
  facts like total working years and age. Good estimates here may
  only be saying "older staff have been here longer".
- Three facts never vary (`EmployeeCount`, `over18`, `StandardHours`)
  and `EmployeeNumber` is just a badge number.
- This data set is widely described as fictional, made by IBM for
  teaching. Check before describing it as real.

**What she can change (proposed):** overTime, businessTravel,
TrainingTimesLastYear, PercentSalaryHike, StockOptionLevel.
**Never to be changed or used as a reason:** Age, gender,
maritalStatus.
**Not hers to change:** everything else (history, role, department,
ratings).

## The twenty asks

| # | she asks | skill |
|--:|---|---|
| 1 | From our 1,470 staff records, show me the working arrangements of the people who stay unusually long. | remember |
| 2 | For someone we have just hired, estimate how long they are likely to stay, from what we know on day one. | guess |
| 3 | People who work overtime seem to leave their role sooner. Is that real, or just noise? | certify |
| 4 | Annual reviews reach me one at a time. Tell me the same day whether this person needs a "what would keep you here" conversation; I will not get to revisit the pile. | flow |
| 5 | Some departments keep people only briefly. What is it about those jobs that explains the short stays? | blame |
| 6 | When you say a team's arrangements are in the top quarter for keeping people, show me where it ranks and why I should believe it. | justify |
| 7 | I can afford in-depth interviews with 50 staff. Using only those, find me the working arrangement that keeps people longest. | choose |
| 8 | Here are 20 kinds of staff who do not stay. What could we actually change for them: travel, overtime, training, pay rise, stock? | fix |
| 9 | These records are typed in by hand. Find the ones that look wrong. | spot |
| 10 | Three advisers have three theories about what keeps people. Give each the same 50 interviews. Who is right? | race |
| 11 | Here is one employee. Show me the people most like them, and how long those people stayed. | remember |
| 12 | If we cut overtime across Sales, what happens to how long people stay? | guess |
| 13 | We added training days last year. Do people with more training really stay longer with their manager? | certify |
| 14 | Survey results come in month by month. Tell me when a team no longer looks the way it normally does. | flow |
| 15 | Which of the things we record have nothing to do with how long people stay, so we can stop collecting them? | blame |
| 16 | Why do you not simply recommend paying everyone more? | justify |
| 17 | Do the same search for our laboratory staff only: the best arrangement for them, interviewing very few. | choose |
| 18 | There is no money for pay this year. What else can we change? | fix |
| 19 | We are about to hire someone unlike anyone we have employed. Tell me when your estimate for them cannot be trusted. | spot |
| 20 | Is your advice any better than our rule of thumb, which is to give the biggest pay rises to the newest staff? | race |

Each skill appears twice. Asks 1 to 10 are the first interview. Asks
11 to 20 came from asking for look-alikes, what-ifs, alerts, why-nots
and special cases until the worries started to repeat.

## A rule for every answer

No recommendation may tell her to change, or select on, a person's
age, gender or marital status. If a skill produces one, record it: it
is an error caught, and it belongs in the report.
