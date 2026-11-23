import csv

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a K-Nearest Neighbors approach based on numeric input features.
    """
    # Identify goal columns: those ending in '+' or '-'
    # The first goal column is 'YearsAtCompany+'
    goal_idx = 31
    
    # Identify input columns (numeric ones that are not goals)
    # Numeric columns start with uppercase.
    input_indices = []
    for i, name in enumerate(header):
        if name[0].isupper() and i != goal_idx and not name.endswith('+') and not name.endswith('-'):
            input_indices.append(i)

    # Normalize training data for distance calculation
    mins = [min(row[i] for row in train) for i in input_indices]
    maxs = [max(row[i] for row in train) for i in input_indices]
    ranges = [maxs[i] - mins[i] if maxs[i] != mins[i] else 1.0 for i in range(len(input_indices))]

    def get_features(row):
        return [(row[idx] - mins[i]) / ranges[i] for i, idx in enumerate(input_indices)]

    train_features = [get_features(row) for row in train]
    predictions = []

    for t_row in test:
        t_feat = get_features(t_row)
        # Find nearest neighbor (simple Euclidean distance)
        best_dist = float('inf')
        best_val = 0.0
        
        for i, feat in enumerate(train_features):
            dist = sum((t_feat[j] - feat[j])**2 for j in range(len(feat)))
            if dist < best_dist:
                best_dist = dist
                best_val = train[i][goal_idx]
        
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
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split: use first 700 to train, next 100 to test
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column for test data
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[31] = "?"
        masked_test.append(new_row)

    results = guess(header, train_data, masked_test)
    
    print("Estimation of 'YearsAtCompany+' for new hires (first 10 samples):")
    for i in range(min(10, len(results))):
        print(f"Test Row {i+1}: Estimated {results[i]:.2f} years")
