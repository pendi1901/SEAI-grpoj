import csv
import random
from step01 import remember

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 16 rows at random.
    2. 'first': Picks the first 16 rows.
    3. 'last': Picks the last 17 rows.
    """
    budget = 50
    strategies = ["random", "first", "last"]
    
    # Define indices for each strategy
    indices = {
        "random": random.sample(range(len(rows)), 16),
        "first": list(range(16)),
        "last": list(range(len(rows) - 17, len(rows)))
    }
    
    results = {}
    best_overall_score = -1.0
    winner = None
    best_row_idx = -1
    
    # Helper to score a row
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    def get_score(row):
        # Normalize goals to [0, 1] based on the whole dataset is not possible here
        # so we use raw values as a proxy for comparison within the labeled set
        return (1.0 - row[mre_idx]) + row[acc_idx] + row[pred_idx]

    for name in strategies:
        strategy_indices = indices[name]
        best_s_score = -1.0
        best_s_idx = -1
        
        for i in strategy_indices:
            goals = label(i)
            # Fill row with goals
            row = list(rows[i])
            for idx, goal_val in zip([mre_idx, acc_idx, pred_idx], goals):
                row[idx] = goal_val
            
            score = get_score(row)
            if score > best_s_score:
                best_s_score = score
                best_s_idx = i
        
        results[name] = (best_s_score, best_s_idx)
        if best_s_score > best_overall_score:
            best_overall_score = best_s_score
            winner = name
            best_row_idx = best_s_idx
            
    return {"winner": winner, "row": best_row_idx, "tried": strategies}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) 
                         for i, val in enumerate(row)])

    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    true_goals = [[r[i] for i in goal_indices] for r in rows]
    
    called = set()
    def label(i):
        if i not in called:
            if len(called) >= 50:
                raise Exception("Budget exceeded")
            called.add(i)
        return true_goals[i]

    masked_rows = []
    for r in rows:
        new_r = list(r)
        for i in goal_indices:
            new_r[i] = "?"
        masked_rows.append(new_r)

    outcome = race(header, masked_rows, label)
    print(f"Race complete. Winner: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
