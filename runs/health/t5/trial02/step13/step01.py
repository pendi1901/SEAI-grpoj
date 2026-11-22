import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses ydist to measure distance to the ideal goal values.
    """
    # Create a table object using the ezr library
    # We prepend the header to the rows to match the expected Tbl input
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
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    # Extract header and rows
    header = next(data_iter)
    rows = list(data_iter)
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Analysis complete. Found {len(best_indices)} highly trustworthy setups.")
    print("Top row indices (0-based):")
    print(best_indices)
    
    # Show a summary of the first best row found
    best_row = rows[best_indices[0]]
    print("\nExample of a top-performing setup:")
    for h, v in zip(header, best_row):
        print(f"  {h}: {v}")
