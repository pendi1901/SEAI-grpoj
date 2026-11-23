import csv

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    Uses a K-Nearest Neighbors approach based on numeric input columns.
    """
    # Identify goal column (first one ending in + or -)
    goal_idx = -1
    for i, col in enumerate(header):
        if col.endswith('+') or col.endswith('-'):
            goal_idx = i
            break
    
    # Identify numeric input columns (starting with uppercase, excluding the goal)
    # We must ensure we only use columns that are actually numeric (floats)
    input_indices = [
        i for i, col in enumerate(header) 
        if col[0].isupper() and i != goal_idx and isinstance(train[0][i], (int, float))
    ]
    
    # Normalize training data for distance calculation
    mins = [min(row[i] for row in train) for i in input_indices]
    maxs = [max(row[i] for row in train) for i in input_indices]
    ranges = [maxs[i] - mins[i] if maxs[i] != mins[i] else 1 for i in range(len(input_indices))]
    
    def get_dist(r1, r2):
        d = 0
        for i, idx in enumerate(input_indices):
            d += ((r1[idx] - r2[idx]) / ranges[i]) ** 2
        return d ** 0.5

    predictions = []
    for t_row in test:
        # Find 5 nearest neighbors in training set
        distances = []
        for train_row in train:
            distances.append((get_dist(t_row, train_row), train_row[goal_idx]))
        
        distances.sort(key=lambda x: x[0])
        
        # Average the goal value of the 5 nearest neighbors
        k = 5
        avg = sum(d[1] for d in distances[:k]) / k
        predictions.append(float(avg))
        
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
                # Columns starting with uppercase are numeric
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split: use first 700 for training, next 100 as test
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    results = guess(header, train_data, masked_test)
    
    print(f"Estimation for first 5 test rows (Goal: {header[goal_idx]}):")
    for i in range(min(5, len(results))):
        print(f"Row {700+i}: Estimated {results[i]:.2f} years")
