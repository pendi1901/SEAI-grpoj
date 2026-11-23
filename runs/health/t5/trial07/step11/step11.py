import ezr
import random

def remember(header, rows):
    """
    Finds the rows most similar to the 'ideal' configuration (the best 
    performing row) and returns their indices.
    """
    # Create a table to handle column roles and distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Identify the best row in the dataset (the one with the lowest ydist)
    # ydist measures how far a row's goals are from the best possible
    scored = []
    for i, row in enumerate(rows):
        scored.append((ezr.ydist(tbl, row), i, row))
    
    # Sort by ydist ascending (lower is better)
    scored.sort(key=lambda x: x[0])
    
    # The 'ideal' setup is the one with the lowest ydist
    ideal_row = scored[0][2]
    
    # Find rows most similar to the ideal_row in the input (X) space
    # xdist measures distance between rows based on input columns
    similarities = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, ideal_row)
        similarities.append((d, i))
    
    # Sort by xdist ascending (smaller distance means more similar)
    similarities.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in similarities[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    best_indices = remember(header, rows)
    
    print("Analysis: Finding setups most similar to the best-performing configuration.")
    print(f"Found {len(best_indices)} configurations similar to the ideal setup.")
    print("Indices of the most similar setups (0-based):")
    print(best_indices)
    
    # Print a summary of the top 3 similar setups
    print("\nTop 3 most similar configurations:")
    tbl = ezr.Tbl([header] + rows)
    for i in best_indices[:3]:
        score = ezr.ydist(tbl, rows[i])
        print(f"Row {i}: ydist={score:.4f} | {rows[i]}")
