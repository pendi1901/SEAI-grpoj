import ezr
import random

def remember(header, rows):
    """
    Identify the best rows based on multi-objective optimization.
    A row is better when its goals (ending in - or +) are closer to their best.
    """
    # Create a temporary table structure to use ezr's ydist logic
    # We need to construct a Tbl object. 
    # ezr.Tbl expects an iterable of rows including the header.
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Sort rows by ydist (distance to ideal goals)
    # Lower ydist is better.
    indexed_rows = list(enumerate(rows))
    indexed_rows.sort(key=lambda x: ezr.ydist(tbl, x[1]))
    
    # Return the top 5% of rows (or at least one)
    limit = max(1, int(len(rows) * 0.05))
    return [idx for idx, row in indexed_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.train.csv"
    all_rows = list(ezr.csv(filename))
    header = all_rows[0]
    rows = all_rows[1:]
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print a short answer for the customer
    print(f"Analysis complete on {len(rows)} records.")
    print(f"Identified {len(best_indices)} setups with the most trustworthy forecasts.")
    print("Indices of top-performing setups:")
    print(best_indices[:10], "..." if len(best_indices) > 10 else "")
    
    # Exit with status 0
    exit(0)
