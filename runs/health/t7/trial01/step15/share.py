import random
from functools import partial
import ezr 
from neighbours import average_nearby_neighbours

def run_race(header, rows, label, strategies):
    if not rows:
        raise ValueError("No rows available to search.")
    copies, trial, tested = setup_trial(header, rows, label)
    found_by = {}
    tried = []
    for name, search, allocation in strategies:
        budget = min(allocation, 50 - len(tested))
        for position in search(header, copies, trial, tested, budget):
            found_by[position] = name
        tried.append(name)
    best = best_positions(header, tested)
    return {"winner": found_by[best], "row": best, "tried": tried}


def biggest_teams(header, rows, trial, tested, budget):
    team = header.index("Team Size")

    def team_size(position):
        value = rows[position][team]
        return float("-inf") if value == "?" else value

    remaining = [i for i in range(len(rows)) if i not in tested]
    selected = sorted(remaining, key=team_size, reverse=True)[:max(0, budget)]
    for position in selected:
        trial(rows[position])
    return selected


def biggest_raises(header, rows, trial, tested, budget):
    pay = header.index("PercentSalaryHike")
    experience = header.index("TotalWorkingYears")

    def priority(position):
        row = rows[position]
        hike = float("-inf") if row[pay] == "?" else row[pay]
        years = float("inf") if row[experience] == "?" else row[experience]
        return -hike, years

    remaining = [i for i in range(len(rows)) if i not in tested]
    selected = sorted(remaining, key=priority)[:max(0, budget)]
    for position in selected:
        trial(rows[position])
    return selected


def setup_trial(header, rows, label, budget =50) : 
    copy = [row.copy() for row in rows]
    positions = {
        id(row) : position for position, row in enumerate(copy)
    }
    table = ezr.Tbl([header] + copy)
    goals =  [column.at for column in table.y]
    tested = {}


    def trial(row):
        position = positions[id(row)]
        if position not in tested:
            if len(tested) >= budget:
                raise ValueError("Budget exceeded")
            values = label(position)
            for at, value in zip(goals, values):
                row[at] = value
            tested[position] = row
        return tested[position]
    return copy, trial, tested
def guided_search(header, rows, trial, tested, budget = 50): 
    positions = {id(row) : i for i, row in enumerate(rows)}
    candidates = [row for i, row in enumerate(rows) if i not in tested]
    count  = min(budget, len(candidates))

    if count <= 0:
        return []
    if count < ezr.the.Start or count == len(candidates):
        selected = random.sample(candidates, count)
        completed = [trial(row) for row in selected]
    else: 
        table = ezr.Tbl([header] + candidates)
        completed = ezr.acquire(table, cap=count, label=trial)

    return [positions[id(row)] for row in completed]

def random_search(header, rows, trial, tested, budget) : 
    positions = [position for position in range(len(rows)) if position not in tested]
    count  = min(budget, len(positions))
    if count <= 0 : 
        return []
    selected = random.sample(positions, count)
    for position in selected : 
        trial(rows[position])
    return selected

def knn_search(header, rows, trial, tested, budget):
    remaining = [
        i for i in range(len(rows))
        if i not in tested
    ]
    selected = []

    def estimated_quality(position):
        return average_nearby_neighbours(
            table, train, rows[position], goal_distance, k=5
        )

    for _ in range(min(budget, len(remaining))):
        if tested:
            train = list(tested.values())
            table = ezr.Tbl([header] + train)
            goal_distance = partial(ezr.ydist, table)

            position = min(remaining, key=estimated_quality)
        else:
            position = random.choice(remaining)

        trial(rows[position])
        selected.append(position)
        remaining.remove(position)

    return selected


def best_positions(header, tested, positions=None): 
    if positions is None: 
        positions  = list(tested)
    else: 
        positions = list(positions)

    if not positions:
        raise RuntimeError("No positions to evaluate")
    
    table = ezr.Tbl([header] + list(tested.values()))
    distance_to_goal = partial(ezr.ydist, table)
    
    def quality(position):
        return distance_to_goal(tested[position])

    return min(positions, key=quality)
