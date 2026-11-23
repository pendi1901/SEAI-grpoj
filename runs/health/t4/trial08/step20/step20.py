import csv
import random
import numpy as np
from step02 import guess
from step09 import spot

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and spotter.
    Total budget: 50 labels.
    """
    budget = 50
    strategies = ["random", "greedy", "spotter"]
    
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    def get_utility(vals):
        # MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
        return -vals[0] + vals[1] + vals[2]

    # Shared tracking to ensure we don't exceed 50 labels
    labelled = {}
    def get_label(i):
        if i not in labelled:
            if len(labelled) >= budget:
                return [0.0, 0.0, 0.0] # Should not happen with careful planning
            labelled[i] = label(i)
        return labelled[i]

    # 1. Random: 16 labels
    random_indices = random.sample(range(len(rows)), 16)
    for i in random_indices:
        get_label(i)
        
    # 2. Greedy: 17 labels (10 train + 7 explore)
    train_indices = random.sample([i for i in range(len(rows)) if i not in labelled], 10)
    train_data = []
    for i in train_indices:
        row = list(rows[i])
        vals = get_label(i)
        row[mre_idx], row[acc_idx], row[pred_idx] = vals
        train_data.append(row)
    
    test_indices = random.sample([i for i in range(len(rows)) if i not in labelled], 7)
    preds = guess(header, train_data, [rows[i] for i in test_indices])
    best_greedy_idx = test_indices[np.argmax(preds)]
    get_label(best_greedy_idx)

    # 3. Spotter: 17 labels
    # Use IsolationForest to find 17 'normal' rows (avoiding outliers)
    suspicious = spot(header, rows)
    safe_indices = [i for i in reversed(suspicious) if i not in labelled][:17]
    for i in safe_indices:
        get_label(i)

    # Evaluate
    results = {}
    for name in strategies:
        best_util = -float('inf')
        best_idx = -1
        if name == "random": subset = random_indices
        elif name == "greedy": subset = train_indices + [best_greedy_idx]
        else: subset = safe_indices
        
        for i in subset:
            util = get_utility(labelled[i])
            if util > best_util:
                best_util = util
                best_idx = i
        results[name] = (best_util, best_idx)

    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": strategies}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)
            
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    # Mask goals for the race
    for row in rows:
        for idx in goal_indices: row[idx] = "?"
        
    res = race(header, rows, label)
    print(f"Race complete. The winning strategy was: {res['winner']}")
    print(f"Best setup found at index: {res['row']}")
    print(f"Strategies compared: {', '.join(res['tried'])}")
    exit(0)
