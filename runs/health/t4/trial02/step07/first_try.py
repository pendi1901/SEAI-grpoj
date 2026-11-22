import csv
import random
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best setup by sampling and using a surrogate model.
    We label 50 rows: 20 random to build a baseline, 30 guided by the model.
    """
    # Identify indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(goals):
        # MRE is minimize, ACC/PRED are maximize.
        # Normalize: (1 - MRE) + ACC + PRED
        return (1.0 - goals[0]) + goals[1] + goals[2]

    labeled_indices = []
    labeled_data = []
    
    # 1. Initial random sampling (20 rows)
    indices = list(range(len(rows)))
    random.shuffle(indices)
    
    for i in indices[:20]:
        goals = label(i)
        labeled_indices.append(i)
        # Store as [mre, acc, pred, ...inputs]
        labeled_data.append(goals + rows[i][3:])
    
    # 2. Iterative improvement (30 rows)
    for _ in range(30):
        # Train model on current labeled data to predict MRE-
        # We use the guess logic from step02
        # Prepare training set
        train_rows = [row for row in labeled_data]
        
        # Prepare test set (all unlabeled rows)
        unlabeled_indices = [i for i in range(len(rows)) if i not in labeled_indices]
        test_rows = [['?'] * 3 + rows[i][3:] for i in unlabeled_indices]
        
        # Predict MRE- (index 0)
        # We need to adapt the guess function's input format
        # For simplicity, we use the logic: train on labeled, predict on unlabeled
        preds = guess(header, train_rows, test_rows)
        
        # Pick the best predicted row
        best_pred_idx = unlabeled_indices[preds.index(min(preds))]
        
        # Label it
        goals = label(best_pred_idx)
        labeled_indices.append(best_pred_idx)
        labeled_data.append(goals + rows[best_pred_idx][3:])
        
    # Find the best among labeled
    best_idx = labeled_indices[0]
    best_score = -float('inf')
    
    for i, idx in enumerate(labeled_indices):
        score = get_score(labeled_data[i][:3])
        if score > best_score:
            best_score = score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i].isupper() or header[i] in ['N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Keep track of calls to label
    call_count = 0
    def label(i):
        global call_count
        call_count += 1
        if call_count > 50:
            raise Exception("Too many labels!")
        # Return true values
        return [rows[i][0], rows[i][1], rows[i][2]]

    best_row_idx = choose(header, rows, label)
    print(f"Best setup found at index: {best_row_idx}")
    print(f"Total setups evaluated: {call_count}")
