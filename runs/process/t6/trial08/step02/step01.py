import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    A row is better if its goals (ending in - or +) are closer to their ideal.
    """
    # Create a table object using the provided header and rows
    # We construct the input as an iterable of rows including the header
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row. 
    # ydist measures how far a row's goals are from the best possible values.
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, as lower is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5% of rows
    limit = max(1, len(rows) // 20)
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
    print("Indices of the best rows (0-based):")
    print(best_indices)
    
    # Display a sample of the best rows
    print("\nSample of best rows:")
    for idx in best_indices[:3]:
        print(f"Row {idx}: {rows[idx]}")
