import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (high score) and is small (low N_estimators).
    We sample 50 rows, label them, and pick the one that maximizes:
    Score = (1 - norm_mre) + norm_acc + norm_pred - norm_n_estimators
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    n_est_idx = header.index('N_estimators')
    
    # Sample 50 indices
    n_rows = len(rows)
    sample_size = min(50, n_rows)
    indices = random.sample(range(n_rows), sample_size)
    
    # Collect data for scoring
    labeled_data = []
    all_n_ests = [r[n_est_idx] for r in rows]
    min_n, max_n = min(all_n_ests), max(all_n_ests)
    
    def norm(val, mn, mx):
        return (val - mn) / (mx - mn) if mx > mn else 0

    # We need to label to get the goals
    for idx in indices:
        goals = label(idx)
        row_with_goals = list(rows[idx])
        for i, g_idx in enumerate(goal_indices):
            row_with_goals[g_idx] = goals[i]
        labeled_data.append((row_with_goals, idx))
    
    # Score based on goals and size (minimize N_estimators)
    # Score = (1-norm_mre) + norm_acc + norm_pred - norm_n_estimators
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    all_mres = [r[mre_idx] for r in rows]
    all_accs = [r[acc_idx] for r in rows]
    all_preds = [r[pred_idx] for r in rows]
    
    best_score = -float('inf')
    best_idx = indices[0]
    
    for row, idx in labeled_data:
        s = (1 - norm(row[mre_idx], min(all_mres), max(all_mres))) + \
            norm(row[acc_idx], min(all_accs), max(all_accs)) + \
            norm(row[pred_idx], min(all_preds), max(all_preds)) - \
            norm(row[n_est_idx], min_n, max_n)
        
        if s > best_score:
            best_score = s
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    true_goals = [[r[i] for i in goal_indices] for r in rows]
    
    masked_rows = []
    for r in rows:
        masked = list(r)
        for i in goal_indices: masked[i] = "?"
        masked_rows.append(masked)

    best_idx = choose(header, masked_rows, lambda i: true_goals[i])
    
    print(f"Recommended setup found at index: {best_idx}")
    print("This setup balances high forecast accuracy with a small footprint (N_estimators).")
    for h, v in zip(header, rows[best_idx]):
        print(f"  {h}: {v}")
