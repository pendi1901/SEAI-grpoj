import ezr
import random

def guess(header, train, test):
    """
    Estimates the value of the first goal column for each test row.
    We build a tree from the training data and use it to predict the 
    goal value for each test row.
    """
    # Create a table from training data to build the model
    tbl = ezr.Tbl([header] + train)
    
    # Build a decision tree based on the training data
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column
    # Goals are columns ending in '+' or '-'
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
            
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        leaf = ezr.leaf(node, row)
        
        # Calculate the mean of the goal column for all rows in this leaf
        vals = [r[goal_idx] for r in leaf.rows if r[goal_idx] != "?"]
        if vals:
            results.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty or has no valid goal data
            all_vals = [r[goal_idx] for r in train if r[goal_idx] != "?"]
            results.append(sum(all_vals) / len(all_vals))
            
    return results

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify indices
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    # Find first goal column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Filter for Sales department
    sales_rows = [r for r in rows if r[dept_idx] == 'Sales']
    
    # Create two scenarios:
    # 1. Current state (keep overtime as is)
    # 2. Counterfactual (force overtime to 'No')
    
    # We use the whole set to train the model
    train = sales_rows
    
    # Test set: all sales rows, but with overtime forced to 'No'
    test_forced = []
    for row in sales_rows:
        new_row = list(row)
        new_row[ot_idx] = 'No'
        new_row[goal_idx] = '?' # Mask the goal
        test_forced.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test_forced)
    
    # Calculate baseline
    actuals = [r[goal_idx] for r in sales_rows]
    
    print("Analysis: Impact of cutting overtime in the Sales department.")
    print("-" * 60)
    print(f"Baseline average tenure: {sum(actuals)/len(actuals):.2f} years")
    print(f"Estimated average tenure if overtime is cut: {sum(estimates)/len(estimates):.2f} years")
    print("-" * 60)
    print("Conclusion: This estimate is derived by simulating the 'No Overtime'")
    print("condition across all Sales employees using a decision tree model.")
