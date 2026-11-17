import ezr
import step01

def spot(header, rows):
    """
    Finds suspicious rows. A row is suspicious if it is an outlier in the 
    input space (x-space) compared to the rest of the data. We use the 
    distance from the centroid of all rows as a measure of suspicion.
    """
    # Create a table to handle column definitions and normalization
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of all rows in x-space
    # We use the cached mids from the table
    centroid = ezr.mids(tbl)
    
    # Calculate distance of each row from the centroid
    # Higher distance = more suspicious
    suspicious = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        suspicious.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 1% most suspicious rows
    limit = max(1, len(rows) // 100)
    return [idx for _, idx in suspicious[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    indices = spot(header, rows)
    
    print(f"Analysis complete on {len(rows)} records.")
    print(f"Identified {len(indices)} potentially erroneous or outlier rows.")
    print("Most suspicious row indices (0-based):")
    print(indices[:10])
    
    print("\nDetails of the most suspicious row:")
    top_idx = indices[0]
    print(f"Row {top_idx}: {rows[top_idx]}")
