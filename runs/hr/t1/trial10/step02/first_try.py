import csv

def guess(header, train, test):
    """
    Estimates the value of the first goal column ('YearsAtCompany+')
    for test rows using a K-Nearest Neighbors approach based on 
    numeric input columns.
    """
    # Find the first goal column index
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    if goal_idx == -1:
        return [0.0] * len(test)

    # Identify numeric input columns (excluding the goal column)
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and i != goal_idx
    ]

    # Simple normalization: calculate ranges for numeric inputs
    mins = [float('inf')] * len(header)
    maxs = [float('-inf')] * len(header)
    for row in train:
        for i in input_indices:
            if row[i] < mins[i]: mins[i] = row[i]
            if row[i] > maxs[i]: maxs[i] = row[i]
    
    ranges = [maxs[i] - mins[i] if maxs[i] != mins[i] else 1.0 for i in range(len(header))]

    predictions = []
    for t_row in test:
        # Find nearest neighbor (Euclidean distance on normalized numeric inputs)
        best_dist = float('inf')
        best_val = 0.0
        
        for train_row in train:
            dist = 0.0
            for i in input_indices:
                diff = (t_row[i] - train_row[i]) / ranges[i]
                dist += diff * diff
            
            if dist < best_dist:
                best_dist = dist
                best_val = train_row[goal_idx]
        
        predictions.append(float(best_val))
        
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
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Use the last 5 rows as a test set
    train_data = rows[:-5]
    test_data = rows[-5:]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    for row in test_data:
        row[goal_idx] = "?"
        
    results = guess(header, train_data, test_data)
    
    print("Estimates for 'YearsAtCompany+' for the last 5 employees:")
    for i, val in enumerate(results):
        print(f"Test Row {i+1}: Estimated {val:.2f} years.")
