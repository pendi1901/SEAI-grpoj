import csv
import random
from step02 import guess
from step09 import spot

def race(header, rows, label):
    """
    Compares three strategies for finding the best row:
    1. 'random': Picks 17 random rows.
    2. 'outliers': Picks 17 rows identified as most suspicious by IsolationForest.
    3. 'tenure': Picks 16 rows with the highest 'YearsAtCompany+' (if available).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Budget: 50 labels total
    strategies = {
        "random": random.sample(range(len(rows)), 17),
        "outliers": spot(header, rows)[:17],
        "tenure": sorted(range(len(rows)), key=lambda i: rows[i][header.index('YearsAtCompany+')], reverse=True)[:16]
    }
    
    # Labeling
    labeled_indices = set()
    for name, indices in strategies.items():
        for idx in indices:
            if idx not in labeled_indices:
                true_goals = label(idx)
                for i, g_idx in enumerate(goal_indices):
                    rows[idx][g_idx] = true_goals[i]
                labeled_indices.add(idx)
    
    # Predict for all rows using the labeled data
    train_data = [rows[i] for i in labeled_indices]
    test_data = [list(r) for r in rows]
    for r in test_data:
        for g_idx in goal_indices:
            r[g_idx] = 0.0 # Dummy for prediction
            
    predictions = guess(header, train_data, test_data)
    
    # Evaluate strategies based on the best row they found
    best_overall_idx = -1
    best_val = -float('inf')
    
    # We evaluate based on the first goal column (YearsAtCompany+)
    target_idx = goal_indices[0]
    
    strategy_results = {}
    for name, indices in strategies.items():
        best_in_strat = -1
        best_val_in_strat = -float('inf')
        for idx in indices:
            val = predictions[idx]
            if val > best_val_in_strat:
                best_val_in_strat = val
                best_in_strat = idx
        strategy_results[name] = (best_in_strat, best_val_in_strat)
        
        if best_val_in_strat > best_val:
            best_val = best_val_in_strat
            best_overall_idx = best_in_strat
            winner = name
            
    return {"winner": winner, "row": best_overall_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Mask goals
    hidden_rows = [list(r) for r in rows]
    for r in hidden_rows:
        for g in goal_indices:
            r[g] = "?"

    def label(i):
        return [rows[i][g] for g in goal_indices]

    result = race(header, hidden_rows, label)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best Row Found: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
