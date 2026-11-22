import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that is both accurate (low ydist) and small (low N_estimators).
    We use a multi-objective approach: we want to minimize ydist AND 
    minimize N_estimators (index 3).
    """
    # 1. Setup
    # We need to label some rows to understand the landscape.
    # We use a budget of 50 labels.
    budget = 50
    labeled = {}
    
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[i] = label(i)
        return labeled[i]

    # 2. Strategy: Active Learning
    # We sample a small initial set to build a model, then use the model
    # to guide us toward rows that are both accurate and small.
    # We define a custom score: ydist + (normalized N_estimators)
    # This balances performance with the "small enough to run nightly" constraint.
    
    # Initial random sample
    indices = random.sample(range(len(rows)), min(len(rows), ezr.the.Start))
    for i in indices:
        get_label(i)
        
    # Build a temporary table with labeled data
    def build_tbl():
        data = [header] + [rows[i] + labeled[i][len(rows[0])-len(header):] 
                           for i in labeled if len(labeled[i]) == len(header)]
        # Note: Since label returns the full row, we just use that.
        return ezr.Tbl([header] + [labeled[i] for i in labeled])

    # Iterative search
    while len(labeled) < budget:
        tbl = build_tbl()
        # Ranker uses the tree to predict ydist
        rank = ezr.ranker(tbl)
        
        # Score unlabeled rows: 
        # We want low ydist (rank) and low N_estimators (index 3)
        # N_estimators is at index 3.
        def score(i):
            r = rows[i]
            # Normalize N_estimators (approx range 50-200)
            n_est_norm = (r[3] - 50) / 150
            return rank(r) + n_est_norm
            
        unlabeled = [i for i in range(len(rows)) if i not in labeled]
        best_i = min(unlabeled, key=score)
        get_label(best_i)
        
    # 3. Final Selection
    # Return the index of the best row found based on the combined score
    final_tbl = build_tbl()
    best_idx = min(labeled.keys(), key=lambda i: ezr.ydist(final_tbl, labeled[i]) + (rows[i][3]/200))
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Mask goals
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return all_rows[i]
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"Optimization complete.")
    print(f"The best setup found (balancing accuracy and model size) is at index {best_idx}.")
    print(f"Setup details: {all_rows[best_idx]}")
    
    exit(0)
