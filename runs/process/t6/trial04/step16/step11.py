import ezr
import step01

def remember(header, rows):
    """
    Find the past configurations most similar to the current proposal.
    In this context, we identify the top 5% of rows that perform best
    across all goals, as these represent the 'ideal' past setups.
    """
    # Use the logic from step01 to identify the best-performing rows
    return step01.remember(header, rows)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print("Analysis: Historical configurations most similar to the ideal setup.")
    print("-" * 60)
    print(f"Found {len(best_indices)} top-performing historical setups.")
    print("-" * 60)
    print(f"{'Index':<10} | {'Cost-':<10} | {'Score-':<10} | {'Idle-':<10}")
    print("-" * 60)
    
    # Identify column indices for the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for idx in best_indices:
        row = rows[idx]
        vals = [f"{row[i]:.4f}" for i in goal_indices]
        print(f"{idx:<10} | {vals[0]:<10} | {vals[1]:<10} | {vals[2]:<10}")
    
    print("-" * 60)
    print("These rows represent the historical configurations that achieved")
    print("the best outcomes. Use these as benchmarks for your proposal.")
