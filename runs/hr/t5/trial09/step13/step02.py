import ezr
import random

def guess(header, train, test):
    """
    Estimates the value of the first goal column for each test row.
    Uses a tree-based approach to find the leaf node containing similar
    historical data and returns the mean value of the first goal column.
    """
    # Create a table object for the training data
    tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree splits based on x-columns to minimize y-distance
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column
    # The goal columns are those ending in + or -
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    first_goal_idx = goal_indices[0]
    
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        values = [r[first_goal_idx] for r in leaf_node.rows if r[first_goal_idx] != "?"]
        if values:
            estimate = sum(values) / len(values)
        else:
            # Fallback to global mean if leaf is empty or has no valid goal data
            all_vals = [r[first_goal_idx] for r in train if r[first_goal_idx] != "?"]
            estimate = sum(all_vals) / len(all_vals)
        results.append(float(estimate))
        
    return results

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test_full = rows[split:]
    
    # Mask the goal columns in the test set to simulate "day one" knowledge
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    test_masked = []
    for row in test_full:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test_masked.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test_masked)
    
    # Print a summary
    first_goal_name = [h for h in header if h.endswith(("+", "-"))][0]
    print(f"Estimated '{first_goal_name}' for {len(estimates)} new hires.")
    print(f"Average predicted value: {sum(estimates)/len(estimates):.2f}")
    print("Sample predictions:")
    for i in range(min(5, len(estimates))):
        print(f"  Hire {i+1}: {estimates[i]:.2f}")
