import ezr
import step01

def spot(header, rows):
    """
    Identify suspicious rows by finding those that are outliers in the 
    input space. We use the distance to the centroid of the data as 
    a measure of 'suspiciousness'. Rows that are far from the center 
    of the input distribution are flagged as potential errors.
    """
    # Create a table to handle the data and calculate distances
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space
    # We use the mids function from ezr which provides the median/mean 
    # for each column.
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # A higher distance indicates the row is an outlier.
    outliers = []
    for i, row in enumerate(rows):
        # xdist calculates the distance between a row and the centroid
        # based on the input columns (X columns).
        dist = ezr.xdist(tbl, row, centroid)
        outliers.append((dist, i))
    
    # Sort by distance descending (most suspicious first)
    outliers.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [idx for dist, idx in outliers[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    # Print results
    print(f"Analysis complete. Found {len(suspicious_indices)} potentially mistyped records.")
    print(f"Most suspicious row indices: {suspicious_indices}")
    
    if suspicious_indices:
        print(f"\nSample of most suspicious row (index {suspicious_indices[0]}):")
        print(rows[suspicious_indices[0]])
    
    exit(0)
