import ezr
import random

def guess(header, train, test):
    """
    Estimates the value of the first goal column for test rows.
    Uses a tree-based approach: train a tree on the labeled data,
    then for each test row, find the leaf and return the mean
    of the first goal column for rows in that leaf.
    """
    # Create a table for training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree nodes contain the rows that fell into that leaf
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Identify the index of the first goal column
    # Goals are columns ending in '+' or '-'
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    first_goal_idx = goal_indices[0]
    
    results = []
    for row in test:
        # Walk the tree to find the leaf for this test row
        node = ezr.leaf(root, row)
        
        # Calculate the mean of the first goal column for all rows in this leaf
        vals = [r[first_goal_idx] for r in node.rows if r[first_goal_idx] != "?"]
        if vals:
            results.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty or has no valid data
            all_vals = [r[first_goal_idx] for r in train if r[first_goal_idx] != "?"]
            results.append(sum(all_vals) / len(all_vals))
            
    return results

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    all_rows = data[1:]
    
    # Split into train (80%) and test (20%)
    random.seed(1234567891)
    random.shuffle(all_rows)
    n = int(len(all_rows) * 0.8)
    train = all_rows[:n]
    test_full = all_rows[n:]
    
    # Mask the goals in the test set to simulate "day one" knowledge
    test_masked = []
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for row in test_full:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test_masked.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test_masked)
    
    # Print summary
    print(f"Estimated tenure for {len(estimates)} test employees.")
    print(f"Average estimated years at company: {sum(estimates)/len(estimates):.2f}")
    print("Sample estimates:")
    for i in range(min(5, len(estimates))):
        print(f"- Employee {i+1}: {estimates[i]:.2f} years")
    
    exit(0)
