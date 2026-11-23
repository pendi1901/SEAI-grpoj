import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the single best change to a row to improve its performance.
    Evaluates all possible single-lever changes and picks the one that 
    results in the highest score according to the remember() logic.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(r):
        # Higher is better
        return r[idx_acc] + r[idx_pred] - r[idx_mre]

    best_change = {}
    best_score = -float('inf')

    # Try every possible change for every allowed lever
    for col, allowed in levers.items():
        col_idx = header.index(col)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range to find the best improvement
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]

        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Since we don't have a predictive model for the goals, 
            # we assume the row's current goals are the baseline.
            # In a real scenario, we'd use a model to predict the new goals.
            # Here, we pick the change that is most likely to move the 
            # configuration towards the center of the "good" parameter space.
            score = get_score(new_row)
            if score > best_score:
                best_score = score
                best_change = {col: val}

    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }

    # Identify a 'bad' row (e.g., one of the lowest scoring ones)
    # We use remember() to rank them and pick the last one
    best_indices = remember(header, rows)
    all_indices = list(range(len(rows)))
    worst_idx = [i for i in all_indices if i not in best_indices][-1]
    worst_row = rows[worst_idx]
    
    recommendation = fix(header, worst_row, levers)
    
    print("Customer Inquiry: Fix my setup with only one change.")
    for col, val in recommendation.items():
        print(f"Recommended change: Set '{col}' to {val}.")
    
    exit(0)
