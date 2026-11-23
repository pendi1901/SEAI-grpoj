import csv

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using 
    a K-Nearest Neighbors approach based on input columns.
    """
    # Identify goal and input columns
    # Goal: MRE- (index 0)
    # Inputs: N_estimators, criterion, Min_sample_leaves, Min_impurity_decrease, Max_depth
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    goal_idx = 0
    
    def distance(row1, row2):
        d = 0
        for i in input_indices:
            val1, val2 = row1[i], row2[i]
            if isinstance(val1, str):
                d += 0 if val1 == val2 else 1
            else:
                # Normalize numeric distance
                d += abs(val1 - val2)
        return d

    predictions = []
    for t_row in test:
        # Find the 5 nearest neighbors in the training set
        distances = []
        for train_row in train:
            distances.append((distance(t_row, train_row), train_row[goal_idx]))
        
        distances.sort(key=lambda x: x[0])
        
        # Average the goal value of the 5 nearest neighbors
        k = 5
        neighbors = distances[:k]
        avg_mre = sum(n[1] for n in neighbors) / k
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
    
    # Split data: 90% train, 10% test (simulated)
    split = int(len(rows) * 0.9)
    train_data = rows[:split]
    test_data = [r[:] for r in rows[split:]]
    
    # Mask the goals in test data
    for row in test_data:
        row[0] = "?"
        row[1] = "?"
        row[2] = "?"
        
    results = guess(header, train_data, test_data)
    
    print("Forecast estimation complete.")
    print(f"Estimated MRE for the first 5 test rows: {[round(x, 4) for x in results[:5]]}")
