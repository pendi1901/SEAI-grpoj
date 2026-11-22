import csv
import numpy as np
import pandas as pd
from step01 import remember

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 17 random rows.
    2. 'biggest_teams': Picks the 17 rows with the highest 'Team Size'.
    3. 'greedy_first': Picks the first 16 rows.
    Total budget: 50 labels.
    """
    budget = 50
    goal_indices = [i for i, col in enumerate(header) if col.endswith('-') or col.endswith('+')]
    team_size_idx = header.index('Team Size')
    
    def get_score(i):
        true_goals = label(i)
        scores = []
        for j, g_idx in enumerate(goal_indices):
            val = true_goals[j]
            # Normalize: '-' minimized (1-val), '+' maximized (val)
            if header[g_idx].endswith('-'):
                scores.append(1.0 - val)
            else:
                scores.append(val)
        return np.mean(scores)

    # Strategy 1: Random
    random_indices = np.random.choice(len(rows), 17, replace=False)
    best_random_idx = -1
    best_random_score = -1
    for i in random_indices:
        s = get_score(i)
        if s > best_random_score:
            best_random_score = s
            best_random_idx = i

    # Strategy 2: Biggest Teams (Customer's current approach)
    # Sort by Team Size descending
    sorted_by_team = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
    best_team_idx = -1
    best_team_score = -1
    for i in sorted_by_team[:17]:
        s = get_score(i)
        if s > best_team_score:
            best_team_score = s
            best_team_idx = i

    # Strategy 3: Greedy First
    best_greedy_idx = -1
    best_greedy_score = -1
    for i in range(16):
        s = get_score(i)
        if s > best_greedy_score:
            best_greedy_score = s
            best_greedy_idx = i

    results = {
        "random": (best_random_score, best_random_idx),
        "biggest_teams": (best_team_score, best_team_idx),
        "greedy_first": (best_greedy_score, best_greedy_idx)
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
        print("Customer Inquiry: Is choosing the biggest teams better than other strategies?")
        print(f"Analysis: The winning strategy was '{result['winner']}'.")
        if result['winner'] == "biggest_teams":
            print("Answer: Yes, your current strategy of picking the biggest teams is effective.")
        else:
            print(f"Answer: No, '{result['winner']}' outperformed your current 'biggest_teams' approach.")
        print(f"Strategies compared: {', '.join(result['tried'])}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
