import ezr
import random

def remember(header, rows):
    """
    Returns the indices of the best rows.
    A row is better when its goals are closer to their best.
    Goals: Cost-, Score-, Idle-.
    """
    # Create a table object to leverage ezr's column handling
    # We prepend the header to the rows to create the table
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for each row.
    # ydist measures how far a row's goals are from the ideal (0.0 for all).
    # Lower ydist is better.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending, so smallest distance first)
    scored.sort(key=lambda x: x[0])
    
    # Return 5% of the rows (800 * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    
    try:
        header = next(rows_gen)
        rows = list(rows_gen)
    except StopIteration:
        exit(1)
        
    best_indices = remember(header, rows)
    
    print(f"Found {len(best_indices)} top-performing setups.")
    print(f"Indices of best rows: {best_indices}")
    print("\nSample of best rows (first 3):")
    for i in best_indices[:3]:
        print(f"Row {i}: {rows[i]}")
    
    exit(0)
