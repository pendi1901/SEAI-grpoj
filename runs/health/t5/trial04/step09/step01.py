import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses the ydist metric from ezr to rank rows by proximity to the ideal.
    """
    # Create a table object to leverage ezr's column and distance logic
    # We prepend the header to the rows to match Tbl expectations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    # ydist measures how far a row is from the ideal goal values
    scored = []
    for i, row in enumerate(rows):
        score = ezr.ydist(tbl, row)
        scored.append((score, i))
    
    # Sort by score (ascending, as ydist 0 is ideal)
    scored.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    header = all_rows[0]
    rows = all_rows[1:]
    
    # Get best indices
    best_indices = remember(header, rows)
    
    # Print results
    print(f"Found {len(best_indices)} trustworthy setups out of {len(rows)}.")
    print("Indices of top-performing rows:")
    print(best_indices)
    
    # Show details of the top 3 for the customer
    print("\nTop 3 setups (MRE-, ACC+, PRED40+):")
    for idx in best_indices[:3]:
        r = rows[idx]
        # Columns 0, 1, 2 are MRE-, ACC+, PRED40+
        print(f"Row {idx}: MRE={r[0]:.3f}, ACC={r[1]:.3f}, PRED40={r[2]:.3f}")
