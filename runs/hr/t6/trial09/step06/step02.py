import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row by finding the 
    nearest neighbor in the training set based on x-columns.
    """
    # Create a table from training data to use ezr's distance functions
    tbl = ezr.Tbl([header] + train)
    
    # Identify the first goal column index
    # Goals are columns ending in '+' or '-'
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    first_goal_idx = goal_indices[0]
    
    results = []
    for t_row in test:
        # Find the row in training data that is closest in x-space
        # xdist uses only the input columns
        best_row = min(train, key=lambda r: ezr.xdist(tbl, t_row, r))
        results.append(best_row[first_goal_idx])
        
    return results

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split into train and test
    # Use a fixed seed for reproducibility
    random.seed(12345)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test = rows[split:]
    
    # Prepare test rows by masking the goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print summary
    print(f"Estimated '{header[goal_indices[0]]}' for {len(estimates)} test cases.")
    print(f"Sample estimate: {estimates[0]:.1f}")
    
    # Calculate mean absolute error for validation
    actuals = [row[goal_indices[0]] for row in test]
    mae = sum(abs(e - a) for e, a in zip(estimates, actuals)) / len(estimates)
    print(f"Mean Absolute Error on test set: {mae:.2f}")
    
    exit(0)
