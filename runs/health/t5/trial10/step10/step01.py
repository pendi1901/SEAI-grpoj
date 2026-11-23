import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses the ydist metric from ezr to find rows closest to the ideal.
    """
    # Create a table object to leverage ezr's column and distance logic
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    # ydist measures how far a row's goals are from the best possible
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending, as lower ydist is better)
    scored.sort()
    
    # Return the top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [idx for _, idx in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis complete. Found {len(best_indices)} highly trustworthy setups.")
    print("Indices of top-performing rows:")
    print(best_indices)
    
    # Show the first few as a sample
    print("\nSample of top-performing rows:")
    for i in best_indices[:3]:
        print(f"Row {i}: {rows[i]}")
    
    exit(0)
