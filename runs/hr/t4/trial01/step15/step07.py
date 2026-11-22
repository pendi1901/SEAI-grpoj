import csv
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows, predicting the goal for the rest,
    and returning the index of the row with the highest predicted goal.
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # We have 800 rows. We can label 50.
    # Strategy: Label the first 50 to train a model, then predict for all.
    labeled_indices = list(range(50))
    
    # Prepare training data
    train_rows = []
    for i in labeled_indices:
        true_vals = label(i)
        row = list(rows[i])
        row[goal_idx] = true_vals[0]
        train_rows.append(row)
        
    # Prepare test data (all rows)
    test_rows = []
    for i in range(len(rows)):
        row = list(rows[i])
        row[goal_idx] = 0.0 # Dummy
        test_rows.append(row)
        
    # Predict for all rows
    predictions = guess(header, train_rows, test_rows)
    
    # Find index of best prediction
    if is_maximize:
        best_idx = max(range(len(predictions)), key=lambda i: predictions[i])
    else:
        best_idx = min(range(len(predictions)), key=lambda i: predictions[i])
        
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Mock label function for the harness
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    def label(i):
        return [rows[i][goal_idx]]
        
    best_row_idx = choose(header, rows, label)
    
    print(f"The best working arrangement found is at row index: {best_row_idx}")
    print(f"Goal value for this row: {rows[best_row_idx][goal_idx]}")
