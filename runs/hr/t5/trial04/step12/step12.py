import ezr
import random

def guess(header, train, test):
    """
    Estimates the value of the first goal column for each test row.
    We use a tree-based approach to find the leaf node containing similar
    historical data and return the mean of the goal column in that leaf.
    """
    # Create table from training data
    tbl = ezr.Tbl([header] + train)
    
    # Build a decision tree based on the training data
    root = ezr.tree(tbl, tbl.rows)
    
    # Identify the first goal column index
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
            
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        leaf_node = ezr.leaf(root, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[goal_idx] for r in leaf_node.rows if r[goal_idx] != "?"]
        if vals:
            results.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty
            all_vals = [r[goal_idx] for r in train if r[goal_idx] != "?"]
            results.append(sum(all_vals) / len(all_vals) if all_vals else 0.0)
            
    return results

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify indices
    dept_idx = header.index('department')
    overtime_idx = header.index('overTime')
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Filter for Sales department
    sales_rows = [r for r in rows if r[dept_idx] == 'Sales']
    
    # Create two scenarios: Current (with overtime) vs Counterfactual (no overtime)
    # We use the existing Sales data to train the model
    train = sales_rows
    
    # Create test rows: Sales employees who currently work overtime
    test_rows = [r for r in sales_rows if r[overtime_idx] == 'Yes']
    
    # Mask the goal and set overtime to 'No' for the counterfactual test
    test_masked = []
    for row in test_rows:
        new_row = list(row)
        new_row[overtime_idx] = 'No'
        new_row[goal_idx] = '?'
        test_masked.append(new_row)
        
    # Estimate the goal (YearsAtCompany+)
    estimates = guess(header, train, test_masked)
    
    # Compare averages
    actual_avg = sum(r[goal_idx] for r in test_rows) / len(test_rows)
    est_avg = sum(estimates) / len(estimates)
    
    print("Analysis: If we cut overtime in Sales, what happens to tenure?")
    print(f"Number of Sales employees currently working overtime: {len(test_rows)}")
    print(f"Average tenure (YearsAtCompany+) with overtime: {actual_avg:.2f} years")
    print(f"Estimated average tenure (YearsAtCompany+) without overtime: {est_avg:.2f} years")
    print(f"Difference: {est_avg - actual_avg:+.2f} years")
    print("\nConclusion: The model suggests that removing overtime in the Sales department "
          "is associated with a change in average tenure as shown above.")
