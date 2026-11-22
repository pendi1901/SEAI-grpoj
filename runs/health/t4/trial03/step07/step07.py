import csv
import random
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best setup by sampling and using a surrogate model.
    We use 50 calls to label() to evaluate candidates.
    """
    # 1. Initial exploration: Label 25 random rows to build a training set
    n_rows = len(rows)
    indices = list(range(n_rows))
    random.shuffle(indices)
    
    labeled_indices = []
    for i in range(25):
        idx = indices[i]
        goals = label(idx)
        # Update row with true values
        for j in range(3):
            rows[idx][j] = goals[j]
        labeled_indices.append(idx)
    
    # 2. Use the remaining 25 calls to label the most promising candidates
    # based on the surrogate model's predictions
    train_data = [rows[i] for i in labeled_indices]
    test_indices = [i for i in range(n_rows) if i not in labeled_indices]
    
    # Prepare test data for guess()
    test_data = [rows[i][:] for i in test_indices]
    for row in test_data:
        for j in range(3):
            row[j] = "?"
            
    # Get predictions for MRE- (the primary goal)
    predictions = guess(header, train_data, test_data)
    
    # Rank test candidates by predicted MRE- (lower is better)
    scored_test = sorted(zip(test_indices, predictions), key=lambda x: x[1])
    
    # Label the top 25 predicted candidates
    for i in range(min(25, len(scored_test))):
        idx = scored_test[i][0]
        goals = label(idx)
        for j in range(3):
            rows[idx][j] = goals[j]
            
    # 3. Final selection: Use remember() logic on all labeled rows
    all_labeled = [rows[i] for i in range(n_rows) if rows[i][0] != "?"]
    best_local_indices = remember(header, all_labeled)
    
    # Map back to original index
    # The remember function returns indices relative to the input list
    # We need to find which of the labeled rows was the best
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
            
    # Keep a copy of true values to simulate the label function
    true_rows = [r[:] for r in rows]
    
    # Mask all goals
    for row in rows:
        for i in range(3):
            row[i] = "?"
            
    def label(i):
        return true_rows[i][:3]
        
    best_idx = choose(header, rows, label)
    print(f"The best setup found is at row index: {best_idx}")
