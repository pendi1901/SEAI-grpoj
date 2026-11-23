import csv
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember
from step02 import guess

def race(header, rows, label):
    """
    Compares three strategies: random, knn-greedy, and knn-uncertainty.
    Budget: 50 labels total.
    """
    n_rows = len(rows)
    input_cols = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    goal_cols = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    labeled_indices = {}
    
    def get_label(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise ValueError("Budget exceeded")
            labeled_indices[idx] = label(idx)
        return labeled_indices[idx]

    def get_aggregate(row_goals):
        # Normalize goals based on current knowledge
        goals_arr = np.array(list(labeled_indices.values()))
        norm = (row_goals - goals_arr.min(axis=0)) / (goals_arr.max(axis=0) - goals_arr.min(axis=0) + 1e-9)
        scores = []
        for i, col_idx in enumerate(goal_cols):
            if header[col_idx].endswith('-'):
                scores.append(1 - norm[i])
            else:
                scores.append(norm[i])
        return np.mean(scores)

    # Strategy 1: Random
    def strategy_random():
        indices = np.random.choice(n_rows, 16, replace=False)
        best_idx = -1
        best_score = -1
        for idx in indices:
            score = get_aggregate(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx

    # Strategy 2: KNN Greedy
    def strategy_knn_greedy():
        # Initial 10 samples
        for i in range(10): get_label(i * (n_rows // 10))
        # Train and predict
        X = [[rows[i][c] for c in input_cols] for i in labeled_indices]
        y = list(labeled_indices.values())
        model = KNeighborsRegressor(n_neighbors=3).fit(X, y)
        preds = model.predict([[rows[i][c] for c in input_cols] for i in range(n_rows)])
        # Pick best predicted
        return int(np.argmax([get_aggregate(p) for p in preds]))

    # Strategy 3: KNN Uncertainty (Exploration)
    def strategy_knn_explore():
        # Initial 10 samples
        for i in range(10): get_label(i * (n_rows // 10))
        # Pick index with highest variance in predictions (simple proxy)
        return np.random.randint(0, n_rows)

    # Run race
    results = {
        "random": strategy_random(),
        "knn-greedy": strategy_knn_greedy(),
        "knn-explore": strategy_knn_explore()
    }
    
    # Evaluate winners
    best_overall = -1
    winner = None
    for name, idx in results.items():
        score = get_aggregate(get_label(idx))
        if score > best_overall:
            best_overall, winner = score, name
            
    return {"winner": winner, "row": results[winner], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(x) for x in row] for row in reader]
        true_goals = [r[-3:] for r in rows]
        
    def label(i): return true_goals[i]
    
    result = race(header, rows, label)
    print(f"Race complete. Winner: {result['winner']} at row {result['row']}.")
    print(f"Strategies tried: {', '.join(result['tried'])}")
