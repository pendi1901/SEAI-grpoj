import csv
import random
from step01 import remember
from step02 import guess
from step09 import spot

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (based on KNN), and outlier-avoidance.
    Budget: 50 labels total.
    """
    budget = 50
    strategies = ["random", "greedy", "spotter"]
    results = {}
    
    # Helper to calculate utility
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    def get_utility(row_vals):
        return -row_vals[mre_idx] + row_vals[acc_idx] + row_vals[pred_idx]

    # Strategy 1: Random
    # Allocate 1/3 of budget
    random_indices = random.sample(range(len(rows)), budget // 3)
    best_random_idx = -1
    best_random_util = -float('inf')
    for idx in random_indices:
        vals = label(idx)
        util = get_utility(vals)
        if util > best_random_util:
            best_random_util = util
            best_random_idx = idx
    results["random"] = (best_random_util, best_random_idx)

    # Strategy 2: Greedy (KNN-based)
    # Use first 10 rows to train, then pick 20 based on best predicted utility
    train_indices = random.sample(range(len(rows)), 10)
    train_data = [rows[i] for i in train_indices]
    for i in train_indices:
        vals = label(i)
        for j, val in enumerate(vals):
            train_data[train_indices.index(i)][[mre_idx, acc_idx, pred_idx][j]] = val
            
    # Predict on remaining, pick top 20
    remaining = [i for i in range(len(rows)) if i not in train_indices]
    preds = guess(header, train_data, [rows[i] for i in remaining])
    # Simple heuristic: assume acc/pred are constant or use KNN for all
    sorted_remaining = sorted(zip(remaining, preds), key=lambda x: -x[1])
    greedy_indices = [x[0] for x in sorted_remaining[:20]]
    
    best_greedy_idx = -1
    best_greedy_util = -float('inf')
    for idx in greedy_indices:
        vals = label(idx)
        util = get_utility(vals)
        if util > best_greedy_util:
            best_greedy_util = util
            best_greedy_idx = idx
    results["greedy"] = (best_greedy_util, best_greedy_idx)

    # Strategy 3: Spotter (Avoid outliers)
    # Use remaining budget (50 - 10 - 20 = 20)
    suspicious = spot(header, rows)
    # Pick 20 that are NOT suspicious
    safe_indices = [i for i in suspicious if i not in train_indices and i not in greedy_indices][-20:]
    best_spot_idx = -1
    best_spot_util = -float('inf')
    for idx in safe_indices:
        vals = label(idx)
        util = get_utility(vals)
        if util > best_spot_util:
            best_spot_util = util
            best_spot_idx = idx
    results["spotter"] = (best_spot_util, best_spot_idx)

    # Determine winner
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
    
    # Mask
    for row in rows:
        for idx in goal_indices: row[idx] = "?"
        
    res = race(header, rows, label)
    print(f"Winner: {res['winner']} at row {res['row']}")
    exit(0)
