import csv
import numpy as np
import pandas as pd
from step01 import remember
from step07 import choose

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (first 50), and top-k (first 50).
    Budget: 50 labels total.
    """
    budget = 50
    goal_indices = [i for i, col in enumerate(header) if col.endswith('-') or col.endswith('+')]
    
    def get_score(i):
        true_goals = label(i)
        scores = []
        for j, g_idx in enumerate(goal_indices):
            val = true_goals[j]
            # Normalize: '-' minimized (1-val), '+' maximized (val)
            # Assuming data is already 0-1 scaled as per problem description
            if header[g_idx].endswith('-'):
                scores.append(1.0 - val)
            else:
                scores.append(val)
        return np.mean(scores)

    # Strategy 1: Random
    random_indices = np.random.choice(len(rows), budget // 3, replace=False)
    best_random_idx = -1
    best_random_score = -1
    for i in random_indices:
        s = get_score(i)
        if s > best_random_score:
            best_random_score = s
            best_random_idx = i

    # Strategy 2: First 50 (Greedy)
    best_greedy_idx = -1
    best_greedy_score = -1
    for i in range(budget // 3):
        s = get_score(i)
        if s > best_greedy_score:
            best_greedy_score = s
            best_greedy_idx = i

    # Strategy 3: Last 50 (End-Greedy)
    best_end_idx = -1
    best_end_score = -1
    for i in range(len(rows) - (budget // 3), len(rows)):
        s = get_score(i)
        if s > best_end_score:
            best_end_score = s
            best_end_idx = i

    results = {
        "random": (best_random_score, best_random_idx),
        "greedy": (best_greedy_score, best_greedy_idx),
        "end-greedy": (best_end_score, best_end_idx)
    }
    
    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals_map = {}
            for i, row in enumerate(reader):
                processed_row = []
                goals = []
                for j, val in enumerate(row):
                    if header[j].endswith('-') or header[j].endswith('+'):
                        goals.append(float(val))
                        processed_row.append("?")
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
                true_goals_map[i] = goals
        
        def label(i):
            return true_goals_map[i]
        
        result = race(header, rows, label)
        print("Customer Inquiry: Which consultant's strategy wins?")
        print(f"Winner: {result['winner']}")
        print(f"Best row found at index: {result['row']}")
        print(f"Strategies compared: {', '.join(result['tried'])}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
