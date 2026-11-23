import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows, 
    accounting for a shift in requirements halfway through the data.
    
    The 'Dynamism' column represents the rate of change. We simulate 
    the effect of requirements changing twice as fast by adjusting 
    the training data to reflect the increased volatility.
    """
    # Identify the index of the first goal column (Cost-)
    goal_idx = [i for i, name in enumerate(header) if name.endswith(('-', '+'))][0]
    
    # We simulate the "twice as fast" requirement change by scaling 
    # the 'Dynamism' input in the training set.
    # We assume the second half of the data represents the high-volatility state.
    n = len(train)
    for i in range(n // 2, n):
        dyn_idx = header.index("Dynamism")
        # Double the dynamism to simulate the increased rate of change
        train[i][dyn_idx] = min(1.0, train[i][dyn_idx] * 2.0)
        
    # Use the existing tree-based estimation logic from step02
    return step02.guess(header, train, test)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Split data: 80% train, 20% test
    n = len(rows)
    split = int(n * 0.8)
    train = rows[:split]
    test_raw = rows[split:]
    
    # Mask the goals in the test set
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    test = []
    for row in test_raw:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    # Print a summary for the customer
    print("Analysis: Impact of doubling requirement change rate on Cost-")
    print("-" * 60)
    print(f"Estimated Cost- for {len(test)} test configurations:")
    print(f"Average estimated cost: {sum(estimates)/len(estimates):.4f}")
    print("-" * 60)
    print("By simulating increased dynamism, we observe how project costs")
    print("react to higher volatility in requirements.")
