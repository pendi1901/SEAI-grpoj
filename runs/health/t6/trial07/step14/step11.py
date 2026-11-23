import ezr
import step01

def remember(header, rows):
    """
    Finds the setups most similar to the 'best' setup found in the data.
    We identify the global best setup, then return the 5% of rows 
    that are most similar (closest in xdist) to that ideal configuration.
    """
    # Create a table to handle column roles and distance calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # 1. Find the global best row (the one with the lowest ydist)
    # We use the logic from step01 to find the best setup
    best_indices = step01.remember(header, rows)
    best_row = rows[best_indices[0]]
    
    # 2. Find rows most similar to the best_row in the input space (xdist)
    # We calculate xdist between every row and the best_row
    similarities = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, best_row)
        similarities.append((d, i))
    
    # 3. Sort by xdist ascending (closest first)
    similarities.sort(key=lambda x: x[0])
    
    # 4. Return the top 5% of rows (excluding the best_row itself if present)
    limit = max(1, int(len(rows) * 0.05))
    results = [item[1] for item in similarities if item[1] != best_indices[0]]
    
    return results[:limit]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Get the similar setups
    indices = remember(header, rows)
    
    # Print a summary for the customer
    print("Analysis complete. Found setups most similar to the top-performing configuration.")
    print(f"Indices of the {len(indices)} most similar setups:")
    print(indices)
    
    # Print details of the first 3
    print("\nSample of similar setups:")
    tbl = ezr.Tbl([header] + rows)
    for i in indices[:3]:
        yd = ezr.ydist(tbl, rows[i])
        print(f"Row {i}: ydist={yd:.3f}, Data={rows[i]}")
