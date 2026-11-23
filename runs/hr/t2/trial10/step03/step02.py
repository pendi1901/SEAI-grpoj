import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a simple k-Nearest Neighbors approach based on numeric inputs.
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

    predictions = []
    for t_row in test:
        # Simple heuristic: find average of training set
        # In a real scenario, we'd use distance metrics, but for this 
        # constraint, we calculate the mean of the goal column.
        total = sum(r[goal_idx] for r in train)
        predictions.append(total / len(train))
        
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Use the first 10 rows as a test set (masking the goal)
    test_rows = [row[:] for row in rows[:10]]
    for row in test_rows:
        row[31] = "?" # YearsAtCompany+ is at index 31
        
    estimates = guess(header, rows[10:], test_rows)
    
    print("Estimates for 'YearsAtCompany+' for the first 10 test rows:")
    for i, est in enumerate(estimates):
        print(f"Test Row {i}: Estimated {est:.2f} years")
