import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses ydist to measure distance to the ideal goal values.
    """
    # Create a table object using the ezr library
    # We prepend the header to the rows to create the TBL structure
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows. 
    # ydist measures how far a row is from the ideal (0.0 distance).
    # We want the smallest ydist.
    indexed_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        indexed_rows.append((d, i))
    
    # Sort by distance (ascending)
    indexed_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in indexed_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Found {len(best_indices)} top-performing setups.")
    print("Indices of the most trustworthy setups (0-based):")
    print(best_indices)
    
    # Show summary of the first few to provide context
    print("\nSummary of the top 3 setups:")
    for i in best_indices[:3]:
        print(f"Row {i}: {rows[i]}")
        
    exit(0)
