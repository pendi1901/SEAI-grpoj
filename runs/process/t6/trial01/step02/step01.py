import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows that perform best across all goals.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    # Create a table object to use ezr's utility functions
    # We construct the input as [header] + rows
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # ydist calculates how far a row is from the ideal (0 for -, 1 for +)
    # We want to minimize ydist.
    scored_rows = []
    for i, row in enumerate(rows):
        # We use the internal ydist logic: 
        # distance from the best possible outcome for all goals
        score = ezr.ydist(tbl, row)
        scored_rows.append((score, i))
    
    # Sort by score (ascending, as lower ydist is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Found {len(best_indices)} top-performing configurations.")
    print(f"{'Index':<10} | {'Goal Distance (ydist)':<20}")
    print("-" * 35)
    
    # Re-calculate table for display purposes
    tbl = ezr.Tbl([header] + rows)
    for idx in best_indices:
        dist = ezr.ydist(tbl, rows[idx])
        print(f"{idx:<10} | {dist:.4f}")
        
    exit(0)
