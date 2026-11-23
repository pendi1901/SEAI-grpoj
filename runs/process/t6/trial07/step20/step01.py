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
    
    # Calculate ydist for every row.
    # ydist calculates how far a row's goals are from the ideal (0 for -, 1 for +).
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, as lower is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    file_path = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(file_path)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty.")
        exit(1)
        
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Found {len(best_indices)} top-performing setups.")
    print("-" * 40)
    print(f"{'Index':<10} | {'Goals Distance (ydist)':<20}")
    print("-" * 40)
    
    # Re-calculate distance for display
    tbl = ezr.Tbl([header] + rows)
    for idx in best_indices:
        dist = ezr.ydist(tbl, rows[idx])
        print(f"{idx:<10} | {dist:.4f}")
        
    exit(0)
