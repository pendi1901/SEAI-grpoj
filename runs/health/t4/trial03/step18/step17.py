import csv
import random
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds a setup that is both performant and small.
    We balance performance (using a surrogate model) and size (N_estimators).
    """
    n_rows = len(rows)
    n_est_idx = header.index('N_estimators')
    
    # 1. Initial exploration: Label 25 random rows to build a training set
    indices = list(range(n_rows))
    random.shuffle(indices)
    
    labeled_indices = []
    for i in range(25):
        idx = indices[i]
        goals = label(idx)
        for j in range(3):
            rows[idx][j] = goals[j]
        labeled_indices.append(idx)
    
    # 2. Use the remaining 25 calls to label candidates.
    # We prioritize candidates that have low N_estimators (small) 
    # and high predicted performance.
    train_data = [rows[i] for i in labeled_indices]
    test_indices = [i for i in range(n_rows) if i not in labeled_indices]
    
    test_data = [rows[i][:] for i in test_indices]
    for row in test_data:
        for j in range(3):
            row[j] = "?"
            
    predictions = guess(header, train_data, test_data)
    
    # Score candidates: (Predicted MRE-) * (N_estimators / Max_N)
    # We want low MRE and low N_estimators.
    max_n = max(r[n_est_idx] for r in rows)
    scored_test = []
    for i, pred in enumerate(predictions):
        idx = test_indices[i]
        # Normalize N_estimators to [0, 1]
        norm_n = rows[idx][n_est_idx] / max_n
        # Combined score: lower is better
        score = pred * norm_n
        scored_test.append((idx, score))
    
    scored_test.sort(key=lambda x: x[1])
    
    # Label the top 25 predicted candidates
    for i in range(min(25, len(scored_test))):
        idx = scored_test[i][0]
        goals = label(idx)
        for j in range(3):
            rows[idx][j] = goals[j]
            
    # 3. Final selection: Use remember() logic on all labeled rows
    all_labeled = [rows[i] for i in range(n_rows) if rows[i][0] != "?"]
    best_local_indices = remember(header, all_labeled)
    
    best_row = all_labeled[best_local_indices[0]]
    for i in range(n_rows):
        if rows[i] == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed)
            
    true_rows = [r[:] for r in rows]
    masked_rows = [r[:] for r in rows]
    for row in masked_rows:
        for i in range(3):
            row[i] = "?"
            
    def label(i):
        return true_rows[i][:3]
        
    best_idx = choose(header, masked_rows, label)
    print(f"The best setup found for performance and nightly runtime is at row index: {best_idx}")
