import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and active learning.
    Budget is 50 labels total.
    """
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    
    df = pd.DataFrame(rows, columns=header)
    labeled_indices = {} # index: goals
    
    def get_score(row_idx):
        if row_idx not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise ValueError("Budget exceeded")
            labeled_indices[row_idx] = label(row_idx)
        
        goals = labeled_indices[row_idx]
        scores = []
        for i, col in enumerate(goal_cols):
            val = float(goals[i])
            # Normalize relative to full dataset range if possible, 
            # but here we use simple min-max of current knowledge
            scores.append(1 - val if col.endswith('-') else val)
        return np.mean(scores)

    # 1. Random Strategy
    random_indices = np.random.choice(len(rows), 16, replace=False)
    for idx in random_indices:
        get_score(idx)
    
    # 2. Greedy Strategy (Pick rows with best inputs based on initial random)
    # Simple heuristic: sum of inputs
    greedy_indices = df[input_cols].sum(axis=1).nlargest(17).index.tolist()
    for idx in greedy_indices:
        get_score(idx)
        
    # 3. Active Learning Strategy
    while len(labeled_indices) < 50:
        train_idx = list(labeled_indices.keys())
        X = df.loc[train_idx, input_cols]
        y = [get_score(i) for i in train_idx]
        model = RandomForestRegressor(n_estimators=10).fit(X, y)
        
        unlabeled = [i for i in range(len(rows)) if i not in labeled_indices]
        preds = model.predict(df.loc[unlabeled, input_cols])
        best_unlabeled = unlabeled[np.argmax(preds)]
        get_score(best_unlabeled)

    # Evaluate
    results = {}
    for name, idxs in [("random", random_indices), ("greedy", greedy_indices), ("active", [i for i in labeled_indices if i not in random_indices and i not in greedy_indices])]:
        scores = {i: get_score(i) for i in idxs}
        best_i = max(scores, key=scores.get)
        results[name] = (best_i, scores[best_i])
        
    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": ["random", "greedy", "active"]}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    df = pd.read_csv(filename)
    header = df.columns.tolist()
    full_data = df.values.tolist()
    rows = [[val if i < 9 else "?" for i, val in enumerate(row)] for row in full_data]
    
    def label(i):
        return full_data[i][9:]
        
    result = race(header, rows, label)
    print(f"Race complete. Winner: {result['winner']} at row {result['row']}.")
    print(f"Strategies tried: {', '.join(result['tried'])}")
