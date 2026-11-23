import csv

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    k-Nearest Neighbors approach based on Euclidean distance of 
    input features.
    """
    # Identify goal and input columns
    goal_idx = 0
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Normalize inputs for distance calculation
    # Only consider numeric inputs for distance
    numeric_inputs = [i for i in input_indices if isinstance(train[0][i], (int, float))]
    
    mins = []
    maxs = []
    for i in numeric_inputs:
        vals = [r[i] for r in train]
        mins.append(min(vals))
        maxs.append(max(vals))
    
    def get_dist(r1, r2):
        d = 0
        for idx, i in enumerate(numeric_inputs):
            rng = maxs[idx] - mins[idx]
            if rng > 0:
                d += ((r1[i] - r2[i]) / rng) ** 2
            # Symbolic columns (criterion) - simple match check
            if header[i] == 'criterion':
                if r1[i] != r2[i]:
                    d += 1
        return d ** 0.5

    predictions = []
    for t_row in test:
        # Find 3 nearest neighbors
        distances = []
        for train_row in train:
            distances.append((get_dist(t_row, train_row), train_row[goal_idx]))
        
        distances.sort(key=lambda x: x[0])
        # Average the goal value of the 3 nearest neighbors
        k = 3
        avg_mre = sum(d[1] for d in distances[:k]) / k
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
                if header[i] in ['criterion']:
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    
    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goals in test data
    masked_test = []
    for r in test_data:
        new_row = list(r)
        new_row[0] = "?" # MRE-
        new_row[1] = "?" # ACC+
        new_row[2] = "?" # PRED40+
        masked_test.append(new_row)
        
    estimates = guess(header, train_data, masked_test)
    
    print("Forecast estimation complete.")
    print(f"Estimated MRE- for first 5 test rows: {[round(e, 4) for e in estimates[:5]]}")
    print(f"Average estimated MRE- across test set: {round(sum(estimates)/len(estimates), 4)}")
