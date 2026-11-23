import ezr
import random

def guess(header, train, test):
    """
    Estimates the value of the first goal column for test rows.
    Uses a tree-based approach to predict the outcome based on input features.
    """
    # Create a table from training data to build the model
    tbl = ezr.Tbl([header] + train)
    
    # Build a tree model using the training data
    # The tree splits based on input features to group similar rows
    root = ezr.tree(tbl, tbl.rows)
    
    # For each test row, find the leaf node it belongs to
    # and return the mean of the first goal column in that leaf
    predictions = []
    
    # Identify the index of the first goal column
    # Goals are columns ending in '+' or '-'
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    first_goal_idx = goal_indices[0]
    
    for row in test:
        # Walk the tree to find the leaf
        node = ezr.leaf(root, row)
        
        # Calculate the mean of the first goal column in this leaf
        # We need to extract the values from the rows in the leaf
        values = [r[first_goal_idx] for r in node.rows if r[first_goal_idx] != "?"]
        
        if values:
            predictions.append(sum(values) / len(values))
        else:
            # Fallback to global mean if leaf is empty or has no valid goal data
            all_vals = [r[first_goal_idx] for r in train if r[first_goal_idx] != "?"]
            predictions.append(sum(all_vals) / len(all_vals))
            
    return predictions

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split into train and test (e.g., 80/20 split)
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test_full = rows[split:]
    
    # Mask the goal columns in the test set to simulate "day one" knowledge
    # The first goal column is 'YearsAtCompany+' (index 31)
    test_masked = []
    for row in test_full:
        new_row = list(row)
        # Mask all goal columns
        for i, name in enumerate(header):
            if name.endswith(("+", "-")):
                new_row[i] = "?"
        test_masked.append(new_row)
        
    # Get predictions
    predictions = guess(header, train, test_masked)
    
    # Print a summary for the customer
    print("Estimation of 'YearsAtCompany' for new hires:")
    for i in range(min(5, len(predictions))):
        print(f"Employee {i+1}: Estimated stay = {predictions[i]:.2f} years")
    
    exit(0)
