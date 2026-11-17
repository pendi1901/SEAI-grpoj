import ezr
import random

def remember(header, rows):
    """
    Returns the indices of the best rows.
    We use the ydist metric from ezr.py, which calculates the distance
    of a row's goals from the ideal (0 for minimize, 1 for maximize).
    """
    # Create a table object to use the library's distance functions
    # We prepend the header to the rows to create the table
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row
    # ydist measures how far a row is from the ideal goal values
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending: smaller distance is better)
    scored.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5% (or at least one)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
    print(f"{'Index':<10} | {'Cost-':<10} | {'Score-':<10} | {'Idle-':<10}")
    print("-" * 45)
    
    # Goal columns are the last three in this specific dataset
    # Cost-, Score-, Idle-
    for idx in best_indices:
        row = rows[idx]
        # Extracting the last 3 columns as per problem description
        c, s, i = row[-3], row[-2], row[-1]
        print(f"{idx:<10} | {c:<10.4f} | {s:<10.4f} | {i:<10.4f}")
    
    exit(0)
