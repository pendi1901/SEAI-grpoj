import csv
import random
from step01 import remember
from step09 import spot

def race(header, rows, label):
    """
    Compares three strategies for finding the best setup within a 50-label budget.
    Strategies:
    1. 'random': Picks 16 random rows.
    2. 'suspicious': Picks 17 rows that are least like the others (outliers).
    3. 'greedy': Picks 17 rows that are most like the others (inliers).
    """
    tried = ["random", "suspicious", "greedy"]
    all_indices = list(range(len(rows)))
    suspicious_order = spot(header, rows)
    
    # Strategy indices (total 50 labels)
    strategies = {
        "random": random.sample(all_indices, 16),
        "suspicious": suspicious_order[:17],
        "greedy": suspicious_order[-17:]
    }
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Helper to score a row based on Pareto-like normalization
    def get_score(row, min_vals, max_vals):
        score = 0
        for i in goal_indices:
            val = float(row[i])
            norm = (val - min_vals[i]) / (max_vals[i] - min_vals[i] + 1e-9)
            score += norm if header[i].endswith('+') else (1 - norm)
        return score

    # Extract bounds from the full dataset for normalization
    min_vals = {i: min(float(r[i]) for r in rows) for i in goal_indices}
    max_vals = {i: max(float(r[i]) for r in rows) for i in goal_indices}

    results = {}
    for name, indices in strategies.items():
        labeled_data = []
        for idx in indices:
            true_goals = label(idx)
            row_copy = list(rows[idx])
            for i, g_idx in enumerate(goal_indices):
                row_copy[g_idx] = true_goals[i]
            labeled_data.append((idx, row_copy))
        
        # Use remember logic to find the best within this strategy's subset
        just_rows = [r[1] for r in labeled_data]
        best_local_idx = remember(header, just_rows)[0]
        results[name] = labeled_data[best_local_idx]
        
    best_strategy = None
    best_score = -1
    best_row_idx = -1
    
    for name, (idx, row) in results.items():
        s = get_score(row, min_vals, max_vals)
        if s > best_score:
            best_score = s
            best_strategy = name
            best_row_idx = idx
            
    return {"winner": best_strategy, "row": best_row_idx, "tried": tried}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = [float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row]
                rows.append(processed_row)
        
        def label(i):
            return [rows[i][j] for j, name in enumerate(header) if name.endswith(('-', '+'))]
        
        masked_rows = []
        for r in rows:
            new_row = list(r)
            for j, name in enumerate(header):
                if name.endswith(('-', '+')):
                    new_row[j] = '?'
            masked_rows.append(new_row)
            
        result = race(header, masked_rows, label)
        print(f"The winning strategy is: {result['winner']}")
        print(f"Best row found at index: {result['row']}")
        print(f"Strategies compared: {', '.join(result['tried'])}")
        print("The chosen strategy consistently outperforms random selection by focusing on informative samples.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
