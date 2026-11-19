import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) for test rows
    by finding the average value of that column from the training set.
    """
    # Find the index of the first goal column ending in '+'
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+'):
            goal_idx = i
            break
    
    if goal_idx == -1:
        return [0.0] * len(test)
    
    # Calculate the average of the goal column from training data
    total = sum(row[goal_idx] for row in train)
    avg_val = total / len(train)
    
    # Return the average for every test row
    return [avg_val] * len(test)

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
    
    # Split data: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal columns in test data as per instructions
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    masked_test = []
    for row in test_data:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
    
    predictions = guess(header, train_data, masked_test)
    
    # Find the first goal column name
    first_goal = [name for name in header if name.endswith('+') or name.endswith('-')][0]
    
    print(f"Estimation for '{first_goal}' based on training average:")
    print(f"Average predicted tenure: {predictions[0]:.2f} years")
    print(f"Estimated for {len(predictions)} test cases.")
