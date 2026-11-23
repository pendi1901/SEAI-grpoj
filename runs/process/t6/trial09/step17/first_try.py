import ezr
import step07

def choose(header, rows, label):
    """
    Find the best setup for a high-stakes project.
    We use the acquire strategy (from step07) which is designed to 
    find the best configurations within a limited labeling budget.
    """
    # We reuse the logic from step07 which implements the acquire strategy.
    # The acquire strategy is robust for multi-objective optimization 
    # and fits the requirement of trialling very few (budget=50).
    return step07.choose(header, rows, label)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    full_data = list(ezr.csv(filename))
    header = full_data[0]
    full_rows = full_data[1:]
    
    # Prepare rows with masked goals as per requirements
    rows = []
    for r in full_rows:
        new_row = r[:]
        for i, h in enumerate(header):
            if h[-1] in "+-":
                new_row[i] = "?"
        rows.append(new_row)
                
    # Define the oracle to reveal true values
    def label(idx):
        return full_rows[idx]
        
    # Run the optimization
    best_idx = choose(header, rows, label)
    
    # Print a summary for the customer
    print("High-Stakes Project Optimization Report:")
    print(f"Optimization complete using a budget of 50 labels.")
    print(f"The best configuration found is at index: {best_idx}")
    print(f"Goal values for this configuration: {full_rows[best_idx][9:]}")
    print("This setup was selected to minimize risk and maximize performance.")
    
    exit(0)
