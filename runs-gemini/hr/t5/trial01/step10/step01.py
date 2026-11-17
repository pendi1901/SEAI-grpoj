import ezr
import random

def remember(header, rows):
    """
    Finds the best rows based on the goals defined in the header.
    Goals ending in '+' are maximized, '-' are minimized.
    """
    # Create a temporary table to use ezr's ydist logic
    # We need to construct a TBL-like object
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    # ydist measures how far a row is from the ideal goal values
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (smallest distance is best)
    scored.sort()
    
    # Return top 5% of rows (or at least one)
    limit = max(1, int(len(rows) * 0.05))
    return [idx for _, idx in scored[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get indices of the best rows
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis of {len(rows)} employee records.")
    print(f"Identified {len(best_indices)} records representing staff with optimal working arrangements.")
    print("-" * 40)
    
    # Show a sample of the best rows
    # We focus on the columns that are goals or key indicators
    goal_cols = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    print("Sample of top-performing records:")
    for idx in best_indices[:3]:
        row = rows[idx]
        summary = {header[i]: row[i] for i in goal_cols}
        print(f"Row {idx}: {summary}")
        
    print("-" * 40)
    print("These employees show the best alignment with organizational goals.")
