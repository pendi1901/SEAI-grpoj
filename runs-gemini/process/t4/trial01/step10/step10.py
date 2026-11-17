import csv
import pandas as pd
import numpy as np
import random
from step01 import remember
from step07 import choose

def race(header, rows, label):
    """
    Compares three strategies: random, remember-based, and choose-based.
    Total budget is 50 labels.
    """
    num_rows = len(rows)
    budget = 50
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(num_rows), budget // 3)
        best_idx = -1
        best_score = float('inf')
        for idx in indices:
            goals = label(idx)
            # Simple score: normalize goals (min=0, max=1)
            # Since we don't have full context, we use raw values as proxy
            score = sum(g if header[i].endswith('-') else -g for i, g in enumerate(goals))
            if score < best_score:
                best_score = score
                best_idx = idx
        return best_idx

    # Strategy 2: Remember (uses top 5% heuristic)
    def strategy_remember():
        # We use the first 100 rows to 'learn' the remember logic, then pick one
        indices = list(range(100))
        best_indices = remember(header, [rows[i] for i in indices])
        idx = best_indices[0]
        label(idx) # Spend 1 label
        return idx

    # Strategy 3: Choose (uses the step07 logic)
    def strategy_choose():
        return choose(header, rows, label)

    strategies = {
        "random": strategy_random,
        "remember": strategy_remember,
        "choose": strategy_choose
    }
    
    results = {}
    for name, func in strategies.items():
        results[name] = func()
        
    # Determine winner based on true goal values
    best_overall_idx = -1
    min_score = float('inf')
    winner = ""
    
    for name, idx in results.items():
        goals = label(idx)
        score = sum(g if header[i].endswith('-') else -g for i, g in enumerate(goals))
        if score < min_score:
            min_score = score
            best_overall_idx = idx
            winner = name
            
    return {"winner": winner, "row": best_overall_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    true_goals = [[float(row[i]) for i in goal_indices] for row in rows]
    
    def label(i):
        return true_goals[i]
    
    result = race(header, rows, label)
    
    print("Customer Inquiry: Three consultants each swear by their own way of picking a setup. Who wins?")
    print(f"Analysis: The winning strategy is '{result['winner']}'.")
    print(f"The best setup found was at row index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
