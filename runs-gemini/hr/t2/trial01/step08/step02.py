import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) for test rows
    by finding the average of the goal column in the training set.
    """
    # Identify the first goal column (ends with '+' or '-')
    goal_idx = -1
    for i, col in enumerate(header):
        if col.endswith('+') or col.endswith('-'):
            goal_idx = i
            break
    
    if goal_idx == -1:
        return [0.0] * len(test)

    # Calculate the mean of the goal column from training data
    goals = [row[goal_idx] for row in train if isinstance(row[goal_idx], (int, float))]
    avg_goal = sum(goals) / len(goals) if goals else 0.0
    
    return [float(avg_goal)] * len(test)

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

    # Create a dummy test row based on the first training row, masking the goal
    test_row = list(rows[0])
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    test_row[goal_idx] = "?"
    
    predictions = guess(header, rows, [test_row])
    
    print("Estimation for new hire:")
    print(f"Predicted {header[goal_idx]}: {predictions[0]:.2f} years")
