import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows that perform best across all goals.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    # Create a table object to leverage ezr's column handling
    # We prepend the header to the rows to create a TBL
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row. 
    # ydist measures how far a row is from the ideal goal values.
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        score = ezr.ydist(tbl, row)
        scored_rows.append((score, i))
    
    # Sort by score (ascending, since lower ydist is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Found {len(best_indices)} top-performing setups out of {len(rows)}.")
    print("Indices of the best rows:")
    print(best_indices)
    
    # Show summary of the first few best rows
    print("\nSample of best rows (first 3):")
    for i in best_indices[:3]:
        print(f"Row {i}: {rows[i]}")
