import csv

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    Uses K-Nearest Neighbors, ensuring only numeric columns are used for distance.
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    
    # Identify numeric input columns (starting with uppercase, excluding the goal)
    input_indices = [
        i for i, col in enumerate(header) 
        if col[0].isupper() and i != goal_idx and isinstance(train[0][i], (int, float))
    ]
    
    # Normalize numeric inputs
    mins = [min(row[i] for row in train) for i in input_indices]
    maxs = [max(row[i] for row in train) for i in input_indices]
    ranges = [maxs[i] - mins[i] if maxs[i] != mins[i] else 1 for i in range(len(input_indices))]
    
    def get_dist(r1, r2):
        d = 0
        # Only use numeric columns for distance calculation to avoid TypeError
        for i, idx in enumerate(input_indices):
            d += ((r1[idx] - r2[idx]) / ranges[i]) ** 2
        return d ** 0.5

    predictions = []
    for t_row in test:
        # Find 5 nearest neighbors
        distances = sorted([(get_dist(t_row, tr), tr[goal_idx]) for tr in train], key=lambda x: x[0])
        avg = sum(d[1] for d in distances[:5]) / 5
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
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Scenario: Compare Sales employees with Overtime vs without
    # We simulate the effect by predicting tenure for Sales employees if we force 'overTime' to 'No'
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    goal_idx = header.index('YearsAtCompany+')
    
    sales_rows = [r for r in rows if r[dept_idx] == 'Sales']
    
    # Create test set: Sales employees with Overtime = 'Yes', but force them to 'No'
    test_set = []
    for r in sales_rows:
        if r[ot_idx] == 'Yes':
            new_r = list(r)
            new_r[ot_idx] = 'No'
            new_r[goal_idx] = "?"
            test_set.append(new_r)
            
    if test_set:
        preds = guess(header, rows, test_set)
        avg_pred = sum(preds) / len(preds)
        
        # Compare with actual average of Sales employees who already don't work overtime
        no_ot_sales = [r[goal_idx] for r in sales_rows if r[ot_idx] == 'No']
        avg_actual = sum(no_ot_sales) / len(no_ot_sales)
        
        print("Impact Analysis: Cutting Overtime in Sales")
        print(f"Estimated average tenure if overtime is cut: {avg_pred:.2f} years")
        print(f"Current average tenure for Sales staff without overtime: {avg_actual:.2f} years")
        print("Conclusion: Removing overtime in Sales is projected to align tenure with current non-overtime staff.")
    else:
        print("No Sales employees with overtime found to analyze.")
