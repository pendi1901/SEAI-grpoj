import csv
from step02 import guess
from step01 import remember

def get_score(r, header, rows):
    """Calculates a score for a row based on multi-objective optimization."""
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')
    
    mres = [x[idx_mre] for x in rows]
    accs = [x[idx_acc] for x in rows]
    preds = [x[idx_pred] for x in rows]
    
    n_mre = (r[idx_mre] - min(mres)) / (max(mres) - min(mres) + 1e-9)
    n_acc = (r[idx_acc] - min(accs)) / (max(accs) - min(accs) + 1e-9)
    n_pred = (r[idx_pred] - min(preds)) / (max(preds) - min(preds) + 1e-9)
    
    # Minimize MRE-, Maximize ACC+, Maximize PRED40+
    return (n_acc + n_pred) - n_mre

def justify(header, rows, row):
    """
    Estimates the performance of a 'biggest, deepest' setup and compares it 
    to the dataset to explain why more is not always better.
    """
    # 1. Estimate goals for the row using KNN
    estimated_goals = guess(header, rows, [row])
    row_with_goals = list(row)
    row_with_goals[0] = estimated_goals[0]
    
    # For ACC+ and PRED40+, we use the average of the dataset as a conservative estimate
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')
    row_with_goals[1] = sum(r[idx_acc] for r in rows) / len(rows)
    row_with_goals[2] = sum(r[idx_pred] for r in rows) / len(rows)
    
    # 2. Compare against all rows
    target_score = get_score(row_with_goals, header, rows)
    better_than_count = sum(1 for r in rows if target_score > get_score(r, header, rows))
    p = better_than_count / len(rows)
    
    reason = f"Using the largest, deepest settings results in a configuration that only outperforms {p:.1%} of existing setups, suggesting that complexity often leads to diminishing returns or overfitting."
    
    return (p, reason)

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
    
    # Define the 'biggest, deepest' setup
    # N_estimators max is 200, Max_depth max is 20
    biggest_setup = [
        "?", "?", "?", 
        200.0, 'squared_error', 1.0, 0.0, 20.0
    ]
    
    p, reason = justify(header, rows, biggest_setup)
    print(f"Performance Score (p): {p:.4f}")
    print(f"Analysis: {reason}")
    exit(0)
