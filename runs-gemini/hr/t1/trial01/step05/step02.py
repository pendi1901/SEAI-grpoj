import csv

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) for test rows
    by finding the average of the goal column in the training set.
    """
    # Identify the first goal column (ends with + or -)
    goal_idx = -1
    for i, col in enumerate(header):
        if col.endswith('+') or col.endswith('-'):
            goal_idx = i
            break
    
    if goal_idx == -1:
        return [0.0] * len(test)

    # Calculate the mean of the goal column from training data
    total = 0.0
    count = 0
    for row in train:
        val = row[goal_idx]
        if isinstance(val, (int, float)):
            total += val
            count += 1
    
    mean_val = total / count if count > 0 else 0.0
    
    # Return the mean for every test row
    return [float(mean_val)] * len(test)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    rows = []
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # For demonstration, we split the data: 90% train, 10% test
    split = int(len(rows) * 0.9)
    train_data = rows[:split]
    test_data = rows[split:]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-'))
    for row in test_data:
        row[goal_idx] = "?"
        
    predictions = guess(header, train_data, test_data)
    
    print(f"Estimation model for '{header[goal_idx]}':")
    print(f"Based on historical data, the average tenure is {predictions[0]:.2f} years.")
    print(f"This estimate is applied to all new hires on day one.")
