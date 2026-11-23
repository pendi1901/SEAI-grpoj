import ezr
import random

def guess(header, train, test):
    """
    Estimates the value of the first goal column for test rows.
    Uses a tree-based approach: train a tree on the labeled data,
    then predict the mean of the leaf node for each test row.
    """
    # Create a table object from the training data
    # ezr.Tbl handles the logic of identifying goals (+/-)
    tbl = ezr.Tbl([header] + train)
    
    # Build a decision tree using the training data
    # The tree splits based on x-columns to minimize y-distance
    root = ezr.tree(tbl, tbl.rows)
    
    # Identify the first goal column index
    # In this dataset, the first goal is 'YearsAtCompany+'
    goal_col = tbl.y[0]
    
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        node = ezr.leaf(root, row)
        
        # Calculate the mean of the goal column for all rows in this leaf
        # We use the column index from the training table
        vals = [r[goal_col.at] for r in node.rows]
        mean_val = sum(vals) / len(vals)
        results.append(mean_val)
        
    return results

if __name__ == "__main__":
    # Load data
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    all_rows = data[1:]
    
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(all_rows)
    split = int(len(all_rows) * 0.8)
    train = all_rows[:split]
    test = all_rows[split:]
    
    # Prepare test rows by masking the goal columns (replacing with "?")
    # The first goal column is at index 31 ('YearsAtCompany+')
    # We mask all goal columns to simulate "day one" knowledge
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
    
    # Get predictions
    predictions = guess(header, train, masked_test)
    
    # Print a summary for the customer
    print("Prediction Summary (YearsAtCompany+):")
    print(f"Estimated average stay for new hires: {sum(predictions)/len(predictions):.2f} years.")
    print(f"Sample prediction for first test case: {predictions[0]:.2f} years.")
    print("-" * 40)
    print("Model uses decision tree leaves to estimate tenure based on initial profile.")
