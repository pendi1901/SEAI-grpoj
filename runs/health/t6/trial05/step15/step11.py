import ezr
import step01

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses the ydist metric from ezr to find rows closest to the ideal.
    """
    # Create a table object to leverage ezr's column and distance logic
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    # ydist measures how far a row is from the ideal goal values
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
    print("Top setups identified based on multi-objective optimization:")
    for idx in best_indices[:5]:
        row = rows[idx]
        # Create a temporary table to calculate the score for display
        tbl = ezr.Tbl([header] + [row])
        score = ezr.ydist(tbl, row)
        print(f"Index {idx}: Score (ydist) = {score:.4f}")
        
    print(f"\nFound {len(best_indices)} highly trustworthy setups.")
    print("These setups minimize MRE and maximize ACC and PRED40.")
