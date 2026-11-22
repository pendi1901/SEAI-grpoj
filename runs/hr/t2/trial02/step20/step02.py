import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) for test rows
    by finding the average value of that column in the training set.
    """
    # Identify the first goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    if goal_idx == -1:
        return [0.0] * len(test)

    # Calculate the average of the goal column from training data
    total = 0.0
    count = 0
    for row in train:
        val = row[goal_idx]
        if isinstance(val, (int, float)):
            total += val
            count += 1
    
    avg = total / count if count > 0 else 0.0
    
    # Return the average for every test row
    return [float(avg)] * len(test)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        new_row.append(float(val))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(val)
            rows.append(new_row)
            
    # Use the first 700 for training, last 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column in test data to simulate "?"
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
            
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    predictions = guess(header, train_data, masked_test)
    
    print("Estimation for new hires (YearsAtCompany+):")
    print(f"Based on historical data, the average tenure is {predictions[0]:.2f} years.")
    print(f"Estimated tenure for {len(predictions)} test cases: {predictions[0]:.2f} years each.")
