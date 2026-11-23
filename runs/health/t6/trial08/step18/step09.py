import ezr
import step01

def spot(header, rows):
    """
    Identify suspicious rows (outliers).
    A row is suspicious if its input values are far from the centroid 
    of the input space (xdist). We calculate the distance of each row 
    from the median input values and return indices of the most distant rows.
    """
    # Create a table to handle column roles and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space (mids)
    # mids() returns a dictionary of the median/mode for each column
    centroids = ezr.mids(tbl)
    
    # Calculate xdist for each row from the centroid
    # Higher xdist means the row is an outlier in the input space
    outliers = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroids)
        outliers.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    outliers.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, int(len(rows) * 0.05))
    return [idx for dist, idx in outliers[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete on {len(rows)} records.")
    print(f"Identified {len(suspicious_indices)} potentially erroneous rows.")
    print("Top 5 most suspicious indices (0-based):", suspicious_indices[:5])
    
    exit(0)
