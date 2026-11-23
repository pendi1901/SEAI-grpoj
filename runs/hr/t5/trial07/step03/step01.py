import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a table object to use ezr's utility functions
    # We need to reconstruct the header with the correct format for ezr
    # ezr expects the header to contain the column names
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows. ydist measures how far a row is from
    # the ideal goal values (0 for '-', 1 for '+').
    # Lower ydist is better.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending) to find the best rows
    scored.sort()
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Found {len(best_indices)} staff records with optimal working arrangements.")
    print("Top performing rows (indices):", best_indices)
    
    # Display the first best row as an example
    best_row = rows[best_indices[0]]
    print("\nExample of a top-performing record:")
    for h, val in zip(header, best_row):
        print(f"  {h}: {val}")
