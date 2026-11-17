# Requirements: setting up an agile programme

**Status: DRAFT.** First draft written by an LLM (Claude) on Nov 16
2026. Not yet edited by the team. Not yet okayed by the lecturer.

## The client

The head of delivery at a software company. She starts several new
programmes a year. For each one she must decide how to staff it and how
to plan the work, knowing some facts about the project that she cannot
change. She pays three bills: the cost of the programme, people sitting
idle while they wait on other teams, and the programme's delivery
score.

## The data

`moot/optimize/process/pom3a.csv`: 20,000 programme setups, each run
through a simulator of agile development. Nine facts per setup, three
results.

| column | in her words |
|---|---|
| Culture | how readily the teams accept changing requirements |
| Criticality | how much damage a failure would do |
| Criticality Modifier | how much extra a critical project costs to build |
| Initial Known | how much of the work is known on day one |
| Inter-Dependency | how much teams must wait on each other |
| Dynamism | how fast the requirements keep changing |
| Size | how big the project is |
| Plan | how the teams decide what to build first |
| Team Size | how many people per team |
| Cost- | what the programme costs (lower is better) |
| Score- | the delivery score, as the data records it (lower is better) |
| Idle- | share of time people sit waiting (lower is better) |

To confirm before coding: the plain reading of each column above comes
from the POM3 description, not from the csv; and `Score-` is marked
"minimise" in the header, which should be checked against the model.

**What she can change (proposed):** Plan, Team Size, Culture.
**What she cannot:** Criticality, Criticality Modifier, Initial Known,
Inter-Dependency, Dynamism, Size. These describe the project, not her
choices.

## The twenty asks

| # | she asks | skill |
|--:|---|---|
| 1 | From the 20,000 setups we have on file, show me the short list that came out unusually well on all three bills. | remember |
| 2 | Before I commit to a setup, tell me roughly what it will cost and how much of the team will sit idle. | guess |
| 3 | Last quarter the small-team setups looked cheaper than the big-team ones. Is that real, or was it luck? | certify |
| 4 | Proposals for new programmes reach my desk one at a time. Tell me on the spot whether to approve each one; I cannot go back. | flow |
| 5 | Why do our worst setups leave so many people waiting around? | blame |
| 6 | When you call a setup "top tier", show me where it ranks against all the others and why I should believe you. | justify |
| 7 | I can afford to trial 50 setups for real. Find me the best one. | choose |
| 8 | This programme is over budget and half idle. What is the smallest change to how we plan and staff it that would rescue it? | fix |
| 9 | Some of these records look mistyped or made up. Point out the ones that do not fit. | spot |
| 10 | Three consultants each swear by their own way of picking a setup. Give each the same 50 trials. Who wins? | race |
| 11 | Here is the setup I am about to propose. Show me the past ones most like it, and how they turned out. | remember |
| 12 | Suppose requirements start changing twice as fast halfway through. What happens to cost and idle time? | guess |
| 13 | In spring we changed how teams decide what to build first. Did results really shift, or are they the same as before? | certify |
| 14 | Results from running programmes arrive week by week. Warn me the moment one starts to go bad. | flow |
| 15 | Which one or two facts about a project matter most to cost, and which can I safely stop worrying about? | blame |
| 16 | I liked setup B. You recommended A. Explain why not B. | justify |
| 17 | This time the project is large and a failure would be very damaging. Find me the best setup for that kind of project, trialling very few. | choose |
| 18 | I am not allowed to hire. What else can I change to cut idle time? | fix |
| 19 | A new team lead proposes a setup unlike anything we have run. Tell me when I am asking you about something you have never seen. | spot |
| 20 | Is your way of choosing any better than what we do now, which is to give every programme the biggest teams we can afford? | race |

Each skill appears twice. Asks 1 to 10 are the first interview. Asks
11 to 20 came from asking for look-alikes, what-ifs, alerts, why-nots
and special cases until the worries started to repeat.
