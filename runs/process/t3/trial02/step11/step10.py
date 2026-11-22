import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (based on KNN), and uncertainty sampling.
    Total budget is 50 labels.
    """
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Helper to score a row
    def get_score(goal_vals):
        score = 0
        for i, g in enumerate(goals):
            val = goal_vals[i]
            if g.endswith('+'):
                score -= val
            else:
                score += val
        return score

    # Track labels
    labeled = {}
    def get_label(idx):
        if idx not in labeled:
            if len(labeled) >= 50:
                raise ValueError("Budget exceeded")
            labeled[idx] = label(idx)
        return labeled[idx]

    # Strategies
    def strategy_random(indices):
        return np.random.choice(indices)

    def strategy_greedy(indices, labeled_indices):
        X_train = [rows[i][:len(inputs)] for i in labeled_indices]
        y_train = [get_label(i) for i in labeled_indices]
        knn = KNeighborsRegressor(n_neighbors=3).fit(X_train, y_train)
        preds = knn.predict([rows[i][:len(inputs)] for i in indices])
        scores = [get_score(p) for p in preds]
        return indices[np.argmin(scores)]

    def strategy_uncertain(indices, labeled_indices):
        # Pick the one furthest from current labeled data (exploration)
        X_train = np.array([rows[i][:len(inputs)] for i in labeled_indices])
        X_pool = np.array([rows[i][:len(inputs)] for i in indices])
        dists = np.min(np.linalg.norm(X_pool[:, np.newaxis] - X_train, axis=2), axis=1)
        return indices[np.argmax(dists)]

    # Run race
    strategies = {"random": strategy_random, "greedy": strategy_greedy, "uncertain": strategy_uncertain}
    results = {name: {"best_idx": -1, "best_score": float('inf')} for name in strategies}
    
    all_indices = list(range(len(rows)))
    # Initial 3 labels (1 per strategy)
    for name in strategies:
        idx = np.random.choice(all_indices)
        results[name]["best_idx"] = idx
        results[name]["best_score"] = get_score(get_label(idx))

    # Remaining 47 labels
    for _ in range(47):
        for name in strategies:
            if len(labeled) >= 50: break
            pool = [i for i in all_indices if i not in labeled]
            if not pool: break
            
            if name == "random":
                idx = strategies[name](pool)
            else:
                idx = strategies[name](pool, list(labeled.keys()))
            
            score = get_score(get_label(idx))
            if score < results[name]["best_score"]:
                results[name]["best_score"] = score
                results[name]["best_idx"] = idx

    winner = min(results, key=lambda n: results[n]["best_score"])
    return {"winner": winner, "row": results[winner]["best_idx"], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row])
        
        true_goals = [row[len(header)-3:] for row in rows]
        def label(i): return true_goals[i]
        
        outcome = race(header, rows, label)
        print(f"The winner is: {outcome['winner']}")
        print(f"Best row found at index: {outcome['row']}")
        print(f"Strategies compared: {', '.join(outcome['tried'])}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
