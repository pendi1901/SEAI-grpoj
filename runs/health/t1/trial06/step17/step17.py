import csv
import random

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing (multi-objective) 
    and 'small' (low N_estimators, low Max_depth).
    """
    budget = 50
    n = len(rows)
    
    # Identify indices
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')
    idx_n = header.index('N_estimators')
    idx_depth = header.index('Max_depth')
    
    # Sample 50 rows
    indices = random.sample(range(n), min(n, budget))
    
    best_idx = -1
    best_score = -float('inf')
    
    # Get global ranges for normalization
    # Since we only have 50 labels, we use them to estimate the range
    labeled_data = []
    for i in indices:
        labeled_data.append((i, label(i)))
        
    mres = [d[1][0] for d in labeled_data]
    accs = [d[1][1] for d in labeled_data]
    preds = [d[1][2] for d in labeled_data]
    
    # Helper to normalize
    def norm(val, min_v, max_v):
        if max_v == min_v: return 0.5
        return (val - min_v) / (max_v - min_v)

    for i, goals in labeled_data:
        # Multi-objective score: 
        # Performance (MRE-, ACC+, PRED40+) + Efficiency (Small N, Small Depth)
        # We want to minimize N and Depth, so we invert them for the score
        mre_n = 1.0 - norm(goals[0], min(mres), max(mres))
        acc_n = norm(goals[1], min(accs), max(accs))
        pred_n = norm(goals[2], min(preds), max(preds))
        
        # Efficiency: lower is better, so we invert
        n_est = rows[i][idx_n]
        depth = rows[i][idx_depth]
        eff_n = 1.0 - (n_est / 200.0)
        depth_n = 1.0 - (depth / 20.0)
        
        # Weighted score: Performance (60%) + Efficiency (40%)
        score = 0.6 * (mre_n + acc_n + pred_n) / 3.0 + 0.4 * (eff_n + depth_n) / 2.0
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith(('-', '+')):
                        goals.append(float(val))
                        processed.append("?")
                    elif header[i] == 'criterion':
                        processed.append(val)
                    else:
                        processed.append(float(val))
                rows.append(processed)
                true_goals.append(goals)
        
        def label(i):
            return true_goals[i]
            
        best_idx = choose(header, rows, label)
        print(f"Best configuration found at index {best_idx}.")
        print(f"This setup balances high performance with low resource usage (N_estimators={rows[best_idx][header.index('N_estimators')]}, Max_depth={rows[best_idx][header.index('Max_depth')]}).")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
