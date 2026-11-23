import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows that perform best across all goals.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    # Create a table object using the provided header and rows
    # The ezr.Tbl function expects an iterable of rows including the header
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the ydist for every row.
    # ydist measures how far a row's goals are from the ideal (0 for -, 1 for +).
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, since lower is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Found {len(best_indices)} top-performing setups out of {len(rows)}.")
    print("Indices of the best rows:")
    print(best_indices)
    
    # Display the first few best rows as a sample
    print("\nSample of top-performing rows (first 3):")
    for i in best_indices[:3]:
        print(f"Row {i}: {rows[i]}")
