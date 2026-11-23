import csv
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Uses a K-Nearest Neighbors approach based on the input columns.
    """
    # Identify goal and input columns
    # Goal: MRE- (index 0)
    # Inputs: N_estimators, criterion, Min_sample_leaves, Min_impurity_decrease, Max_depth
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    def get_distance(row1, row2):
        dist = 0
        for i in input_indices:
            val1, val2 = row1[i], row2[i]
            if isinstance(val1, str):  # Symbolic column: criterion
                dist += 0 if val1 == val2 else 1.0
            else:  # Numeric column
                # Simple normalized distance
                dist += abs(val1 - val2)
        return dist

    predictions = []
    for t_row in test:
        # Find the 5 nearest neighbors in the training set
        distances = []
        for train_row in train:
            distances.append((get_distance(t_row, train_row), train_row[0]))
        
        distances.sort(key=lambda x: x[0])
        # Average the MRE- of the 5 nearest neighbors
        neighbors = distances[:5]
        avg_mre = sum(n[1] for n in neighbors) / len(neighbors)
        predictions.append(avg_mre)
        
    return predictions

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
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

    # Split into train and a small test set for demonstration
    train_data = rows[:700]
    test_data = [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]] for r in rows[700:710]]
    # Mask the goals in test data
    for r in test_data:
        r[0] = r[1] = r[2] = "?"

    results = guess(header, train_data, test_data)
    
    print("Estimated MRE- for the first 10 test rows:")
    for i, val in enumerate(results):
        print(f"Row {i+1}: {val:.4f}")
    
    exit(0)
