import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal (MRE-) for test rows using a K-Nearest Neighbors 
    approach based on the input features (non-goal columns).
    """
    # Identify indices
    goal_idx = 0  # MRE-
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Pre-calculate numeric ranges for normalization to handle distance
    input_data = []
    for row in train:
        input_data.append([row[i] for i in input_indices])
    
    # Simple distance function: Euclidean for numeric, equality for symbolic
    def dist(row1, row2):
        d = 0
        for i, idx in enumerate(input_indices):
            val1, val2 = row1[idx], row2[idx]
            if isinstance(val1, float):
                # Normalize by range if possible, else simple diff
                d += (val1 - val2) ** 2
            else:
                d += 0 if val1 == val2 else 1
        return d ** 0.5

    predictions = []
    for t_row in test:
        # Find nearest neighbor in training set
        best_d = float('inf')
        best_val = 0
        for train_row in train:
            d = dist(t_row, train_row)
            if d < best_d:
                best_d = d
                best_val = train_row[goal_idx]
        predictions.append(best_val)
    
    return predictions

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    # Numeric columns: MRE-, ACC+, PRED40+, N_estimators, 
                    # Min_sample_leaves, Min_impurity_decrease, Max_depth
                    if header[i] not in ['criterion']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Split: use first 700 for training, next 100 for testing
        train_data = rows[:700]
        test_data = [[r[0] if i > 2 else '?' for i, r in enumerate(row)] for row in rows[700:800]]
        
        results = guess(header, train_data, test_data)
        
        print("Forecast Analysis:")
        print(f"Estimated MRE- for the first 5 test setups: {[round(x, 4) for x in results[:5]]}")
        print("These estimates are based on the nearest neighbor performance in the training set.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
