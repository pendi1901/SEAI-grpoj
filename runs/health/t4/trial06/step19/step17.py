import csv
import random
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds a setup that is both accurate (low MRE-) and small (low N_estimators).
    We use a budget of 50 labels to explore the space and identify a 
    Pareto-optimal configuration that balances performance and size.
    """
    # Budget: 50 labels
    budget = 50
    tried = {}
    
    # Helper to get true goals and update the row
    def get_true_row(idx):
        if idx not in tried:
            if len(tried) >= budget:
                return None
            goals = label(idx)
            tried[idx] = goals
            # Fill in the row
            goal_cols = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
            for i, g_idx in enumerate(goal_cols):
                rows[idx][g_idx] = goals[i]
        return rows[idx]

    # Strategy: Sample random rows to get a baseline, then use the model
    # to predict performance for the remaining rows and pick the best trade-off.
    
    # 1. Initial exploration: sample 25 random rows
    indices = random.sample(range(len(rows)), min(25, len(rows)))
    for idx in indices:
        get_true_row(idx)
        
    # 2. Use model to predict MRE- for all rows
    # Prepare training data
    train_indices = list(tried.keys())
    train_data = [rows[i] for i in train_indices]
    
    # Predict for all rows
    all_preds = guess(header, train_data, rows)
    
    # 3. Score rows based on MRE- (predicted) and N_estimators (size)
    # We want to minimize MRE- and minimize N_estimators
    n_idx = header.index('N_estimators')
    
    best_idx = -1
    best_score = float('inf')
    
    for i in range(len(rows)):
        mre_pred = all_preds[i]
        n_est = float(rows[i][n_idx])
        
        # Simple weighted objective: normalize and sum
        # Since we want small and accurate, we minimize this score
        score = (mre_pred * 0.7) + ((n_est / 200.0) * 0.3)
        
        if score < best_score:
            best_score = score
            best_idx = i
            
    # Ensure the best one is labeled
    get_true_row(best_idx)
    
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    # Keep original for labeling
    original_rows = [list(r) for r in rows]
    def label(i):
        return [original_rows[i][j] for j, h in enumerate(header) if h.endswith(('-', '+'))]

    # Hide goals
    for r in rows:
        for j, h in enumerate(header):
            if h.endswith(('-', '+')): r[j] = "?"

    best_idx = choose(header, rows, label)
    print(f"Recommended configuration index: {best_idx}")
    print("This setup balances low MRE- (accuracy) with low N_estimators (runtime).")
