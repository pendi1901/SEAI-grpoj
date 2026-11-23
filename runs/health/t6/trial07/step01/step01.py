import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses the ydist metric from ezr to rank rows by their proximity to the 
    ideal goal values.
    """
    # Create a table object to leverage ezr's column handling and ydist
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    # ydist measures how far a row's goals are from the best possible values
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending, as lower ydist is better)
    scored.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis complete. Found {len(best_indices)} highly trustworthy setups.")
    print("Indices of the top-performing rows:")
    print(best_indices)
    
    # Print details of the top 3 as a sample
    print("\nTop 3 recommended setups:")
    for i in best_indices[:3]:
        print(f"Row {i}: {rows[i]}")
