import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a table object to use ezr's utility functions
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows. 
    # ydist measures how far a row is from the ideal goal values.
    # We want to minimize ydist.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending) to find the "best" rows
    scored.sort()
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get indices of the best rows
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis of {len(rows)} employee records.")
    print(f"Identified {len(best_indices)} employees with optimal working arrangements.")
    print("\nTop performing rows (indices):", best_indices)
    
    # Show a sample of the best rows
    print("\nSample of best records:")
    for idx in best_indices[:3]:
        row = rows[idx]
        # Display key columns: YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+
        # These are at indices 31, 32, 34
        print(f"Row {idx}: YearsAtCompany={row[31]}, YearsInRole={row[32]}, YearsWithManager={row[34]}")
