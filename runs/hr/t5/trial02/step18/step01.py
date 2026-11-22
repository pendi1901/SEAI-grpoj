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
    
    # Calculate ydist for all rows
    # ydist measures how far a row is from the ideal goal values
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (lower is better)
    scored.sort()
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
    return [i for d, i in scored[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get best indices
    best_indices = remember(header, rows)
    
    # Print results
    print(f"Found {len(best_indices)} top-performing employee records.")
    print("These employees represent the best working arrangements based on the provided goals.")
    
    # Display a summary of the first best row found
    best_row = rows[best_indices[0]]
    print("\nExample of a top-performing record:")
    for name, val in zip(header, best_row):
        print(f"  {name}: {val}")
    
    exit(0)
