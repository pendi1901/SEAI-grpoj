import csv

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a k-Nearest Neighbors approach, considering only numeric inputs.
    """
    # Identify the first goal column
    goal_cols = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    goal_idx = goal_cols[0]
    
    # Identify numeric input columns (excluding goals and non-numeric columns)
    # A column is numeric if the header starts with an uppercase letter
    input_indices = [
        i for i, h in enumerate(header) 
        if h[0].isupper() and i != goal_idx
    ]
    
    # Normalize data for distance calculation (min-max)
    mins = [min(row[i] for row in train) for i in input_indices]
    maxs = [max(row[i] for row in train) for i in input_indices]
    ranges = [maxs[j] - mins[j] if maxs[j] != mins[j] else 1.0 for j in range(len(input_indices))]
    
    def get_dist(r1, r2):
        d = 0.0
        for j, idx in enumerate(input_indices):
            d += ((r1[idx] - r2[idx]) / ranges[j])**2
        return d**0.5

    predictions = []
    for t_row in test:
        # Find nearest neighbor in training set
        best_dist = float('inf')
        best_val = 0.0
        for train_row in train:
            d = get_dist(t_row, train_row)
            if d < best_dist:
                best_dist = d
                best_val = train_row[goal_idx]
        predictions.append(float(best_val))
        
    return predictions

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                # Numeric columns start with uppercase
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split: use first 700 to train, next 100 to test
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column for test data
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    results = guess(header, train_data, masked_test)
    
    print(f"Estimated tenure for {len(results)} new hires:")
    for i in range(min(5, len(results))):
        print(f"Hire {i+1}: Predicted {header[goal_idx]} = {results[i]:.2f} years")
