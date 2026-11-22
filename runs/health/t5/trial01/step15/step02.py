import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row by finding the 
    nearest neighbor in the training set based on x-column distance.
    """
    # Create a table object for the training data
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Identify the index of the first goal column
    # The first goal column is the first one ending in '-' or '+'
    goal_idx = -1
    for i, name in enumerate(header):
        if name[-1] in "+-":
            goal_idx = i
            break
            
    results = []
    for t_row in test:
        # Find the row in training data that is closest in x-space
        # We use xdist from ezr which compares only input columns
        best_row = min(train, key=lambda r: ezr.xdist(tbl, t_row, r))
        results.append(best_row[goal_idx])
        
    return results

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(all_rows)
    split = int(len(all_rows) * 0.8)
    train = all_rows[:split]
    test_raw = all_rows[split:]
    
    # Mask the goals in the test set to simulate "unknown"
    test = []
    for row in test_raw:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    # Calculate average error for the test set (first goal column)
    goal_idx = next(i for i, name in enumerate(header) if name[-1] in "+-")
    actuals = [row[goal_idx] for row in test_raw]
    
    errors = [abs(est - act) for est, act in zip(estimates, actuals)]
    avg_error = sum(errors) / len(errors)
    
    print(f"Forecast analysis complete.")
    print(f"Estimated the first goal column for {len(test)} test cases.")
    print(f"Average absolute error of forecasts: {avg_error:.4f}")
    
    exit(0)
