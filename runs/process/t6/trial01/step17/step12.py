import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows.
    To simulate 'requirements changing twice as fast', we weight the 
    training rows based on their 'Dynamism' (index 5). 
    Rows with higher Dynamism are given more weight in the tree model 
    to reflect the increased volatility.
    """
    # Dynamism is at index 5
    # Cost- is at index 9
    
    # We create a weighted training set by duplicating rows with high Dynamism
    # This biases the tree model towards the 'faster changing' requirements
    weighted_train = []
    for row in train:
        dynamism = row[5]
        # Weight factor: higher dynamism = more representation
        weight = int(dynamism * 10) + 1
        for _ in range(weight):
            weighted_train.append(row)
            
    # Use the logic from step02 to estimate the goal
    return step02.guess(header, weighted_train, test)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Split data: 80% train, 20% test
    split_idx = int(len(all_rows) * 0.8)
    train = all_rows[:split_idx]
    test_raw = all_rows[split_idx:]
    
    # Mask the goals in the test set
    test = []
    for row in test_raw:
        new_row = row[:]
        new_row[9] = new_row[10] = new_row[11] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    print("Analysis: Impact of increased requirements volatility (Dynamism).")
    print(f"Estimated average Cost- under high-volatility model: {sum(estimates)/len(estimates):.4f}")
    print("By weighting high-dynamism configurations, we account for the increased")
    print("cost and idle time associated with faster-changing requirements.")
    
    exit(0)
