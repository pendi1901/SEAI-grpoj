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
    
    if goal_idx == -1:
        return [0.0] * len(test)

    # Identify numeric input columns (excluding the goal column)
    # Ensure we only use columns that are actually numeric (float)
    input_indices = [
        i for i, col in enumerate(header) 
        if col[0].isupper() and i != goal_idx
    ]

    predictions = []
    for t_row in test:
        distances = []
        for r_row in train:
            dist = 0.0
            for i in input_indices:
                # Ensure both values are numeric before subtraction
                val_t = t_row[i]
                val_r = r_row[i]
                if isinstance(val_t, (int, float)) and isinstance(val_r, (int, float)):
                    dist += abs(val_t - val_r)
                else:
                    # If data is missing or non-numeric, add a penalty
                    dist += 1.0
            distances.append((dist, r_row[goal_idx]))
        
        # Find the average of the goal value for the 5 nearest neighbors
        distances.sort(key=lambda x: x[0])
        k = 5
        neighbors = distances[:k]
        avg_val = sum(n[1] for n in neighbors) / k
        predictions.append(float(avg_val))
        
    return predictions

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                # Convert numeric columns (starting with uppercase)
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split data: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-'))
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
    
    results = guess(header, train_data, masked_test)
    
    print(f"Estimated tenure for the first 5 test cases:")
    for i in range(min(5, len(results))):
        print(f"Test Row {i}: Estimated {header[goal_idx]} = {results[i]:.2f} years")
