import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (best of sample), and surrogate.
    Budget: 50 labels total.
    """
    budget = 50
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    def evaluate(idx):
        goals = get_label(idx)
        # Normalize goals (using full dataset range is not possible, 
        # so we use a simple aggregate of the goals provided)
        # Since we need to compare, we just use the raw values for simplicity
        # or a basic heuristic.
        return sum(goals) # Placeholder: logic depends on goal direction

    # Strategy 1: Random
    def strategy_random():
        indices = np.random.choice(len(rows), 16, replace=False)
        best_idx = -1
        best_val = float('inf')
        for i in indices:
            val = sum(get_label(i))
            if val < best_val:
                best_val = val
                best_idx = i
        return best_idx

    # Strategy 2: Greedy (Sample first 16)
    def strategy_greedy():
        best_idx = -1
        best_val = float('inf')
        for i in range(16):
            val = sum(get_label(i))
            if val < best_val:
                best_val = val
                best_idx = i
        return best_idx

    # Strategy 3: Surrogate (Sample 18, train RF, predict best)
    def strategy_surrogate():
        sample_indices = np.linspace(0, len(rows) - 1, 18, dtype=int)
        train_x = [[rows[i][j] for j, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))] for i in sample_indices]
        train_y = [get_label(i) for i in sample_indices]
        
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(train_x, train_y)
        
        all_x = [[rows[i][j] for j, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))] for i in range(len(rows))]
        preds = model.predict(all_x)
        best_idx = int(np.argmin([sum(p) for p in preds]))
        return best_idx

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "surrogate": strategy_surrogate
    }

    results = {}
    for name, func in strategies.items():
        idx = func()
        results[name] = (idx, sum(get_label(idx)))

    winner = min(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        true_goals = []
        for row in reader:
            processed = []
            goals = []
            for i, val in enumerate(row):
                if header[i].endswith(('-', '+')):
                    goals.append(float(val))
                    processed.append("?")
                else:
                    processed.append(float(val))
            rows.append(processed)
            true_goals.append(goals)

    def label(i):
        return true_goals[i]

    res = race(header, rows, label)
    print(f"The winning strategy is: {res['winner']}")
    print(f"Best row found at index: {res['row']}")
    print(f"Strategies compared: {', '.join(res['tried'])}")
