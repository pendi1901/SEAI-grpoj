import random
from functools import partial
import ezr 

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
                return ValueError("Budget exceeded")
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

    if count == 0:
        return []
    if count < ezr.the.Start or count == len(candidates):
        selected = random.sample(candidates, count)
        completed = [trial(row) for row in selected]
    else: 
        table = ezr.Tbl([header] + candidates)
        completed = ezr.acquire(table, cap=count, label=trial)

    return [positions[id(row)] for row in completed]

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