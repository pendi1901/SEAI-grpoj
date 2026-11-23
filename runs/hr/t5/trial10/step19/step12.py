import ezr
import random

def guess(header, train, test):
    """
    Estimates the 'YearsAtCompany+' (first goal column) for test rows
    after simulating a policy change: setting 'overTime' to 'No' 
    for all employees in the 'Sales' department.
    """
    # Identify indices
    overtime_idx = header.index("overTime")
    dept_idx = header.index("department")
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    first_goal_idx = goal_indices[0]

    # Apply the policy change to the test set
    modified_test = []
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == "Sales":
            new_row[overtime_idx] = "No"
        modified_test.append(new_row)

    # Build a model on the training data
    tbl = ezr.Tbl([header] + train)
    root = ezr.tree(tbl, tbl.rows)

    # Predict the first goal for the modified test rows
    predictions = []
    for row in modified_test:
        node = ezr.leaf(root, row)
        values = [r[first_goal_idx] for r in node.rows if r[first_goal_idx] != "?"]
        if values:
            predictions.append(sum(values) / len(values))
        else:
            # Fallback to global mean
            all_vals = [r[first_goal_idx] for r in train if r[first_goal_idx] != "?"]
            predictions.append(sum(all_vals) / len(all_vals))
            
    return predictions

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split data
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test_full = rows[split:]
    
    # Mask goals for test
    test_masked = []
    for row in test_full:
        new_row = list(row)
        for i in range(len(header)):
            if header[i].endswith(("+", "-")):
                new_row[i] = "?"
        test_masked.append(new_row)
        
    # Get predictions
    preds = guess(header, train, test_masked)
    
    # Summary
    print("Policy Analysis: Impact of cutting overtime in Sales on 'YearsAtCompany'.")
    print(f"Estimated average years at company for Sales staff after policy change: {sum(preds)/len(preds):.2f} years.")
    print("This estimate is based on a tree-based model trained on existing employee data.")
    
    exit(0)
