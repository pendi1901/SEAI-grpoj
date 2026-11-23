import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses the ydist metric from ezr to rank rows by their proximity to the 
    ideal goal values.
    """
    # Create a table object to leverage ezr's column and distance logic
    # The header is required to build the table structure
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row. 
    # ydist measures how far a row's goals are from the best possible values.
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, since lower is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [idx for score, idx in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    # Extract header and rows
    header = next(data_iter)
    rows = list(data_iter)
    
    # Get the best row indices
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis complete on {len(rows)} records.")
    print(f"Identified {len(best_indices)} setups with the most trustworthy forecasts.")
    print("Top 5 indices (0-based):", best_indices[:5])
    
    # Exit with status 0
    exit(0)
