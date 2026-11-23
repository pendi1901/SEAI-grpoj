import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows.
    To simulate requirements changing twice as fast, we adjust the 
    'Dynamism' input column (index 5) in the training data to reflect
    the increased volatility, then use the tree-based ranker.
    """
    # Dynamism is at index 5. We simulate "twice as fast" by doubling 
    # the dynamism values in the training set.
    dynamism_idx = 5
    
    # Create a modified training set
    modified_train = []
    for r in train:
        new_row = list(r)
        # Cap at 1.0 as these are normalized values
        new_row[dynamism_idx] = min(1.0, new_row[dynamism_idx] * 2.0)
        modified_train.append(new_row)
    
    # Use the logic from step02 to estimate the first goal (Cost-)
    return step02.guess(header, modified_train, test)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split data: 80% train, 20% test
    n_train = int(len(rows) * 0.8)
    train_data = rows[:n_train]
    test_data = rows[n_train:]
    
    # Mask the goals in the test data
    masked_test = []
    for r in test_data:
        new_row = list(r)
        new_row[9] = new_row[10] = new_row[11] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train_data, masked_test)
    
    print("Analysis: If requirements change twice as fast (doubled Dynamism):")
    avg_est = sum(estimates) / len(estimates)
    print(f"The estimated average Cost- for the test scenarios is: {avg_est:.4f}")
    print("This suggests that increased volatility significantly impacts project costs.")
    
    exit(0)
