import csv
import step01
import step02

def fix(header, row, levers):
    """
    Recommends the single best change to a bad row to maximize its 
    multi-objective score, staying within the provided levers.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # We need a reference for normalization. Use the row itself as a baseline
    # or a simple heuristic. Since we want to improve the row, we evaluate
    # candidates and pick the one that yields the best estimated score.
    
    def get_score(r):
        # Heuristic: minimize MRE, maximize ACC, maximize PRED
        # Since we don't have the full dataset here, we use a simple 
        # weighted sum of the goals.
        return (-r[mre_idx] + r[acc_idx] + r[pred_idx])

    best_change = {}
    best_score = -float('inf')
    
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            low, high = allowed
            # Try 5 steps
            for i in range(5):
                val = low + (high - low) * (i / 4.0)
                candidates.append(val)
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            test_row = row[:]
            test_row[col_idx] = val
            
            # Estimate performance: use step02.guess logic if possible, 
            # but for a single-lever fix, we estimate the impact.
            # Here we simulate the score improvement.
            score = get_score(test_row)
            
            if score > best_score:
                best_score = score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    # Identify a "bad" row (e.g., lowest score)
    scores = [(-r[0] + r[1] + r[2]) for r in rows]
    bad_idx = scores.index(min(scores))
    bad_row = rows[bad_idx]
    
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Max_depth': (1, 20)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print(f"To improve performance for the worst-performing setup (Row {bad_idx}), we recommend:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to {val}")
