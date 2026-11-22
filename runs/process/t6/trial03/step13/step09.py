import ezr
import step01

def spot(header, rows):
    """
    Identify rows that are 'outliers' in the input space.
    We use the distance from the centroid of the data as a measure of suspicion.
    Rows that are far from the center of the input space are most suspicious.
    """
    # Create a table to handle normalization and distance calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the centroid (mids) of the input columns
    centroid = ezr.mids(tbl)
    
    # Calculate xdist for each row from the centroid
    # Higher xdist means the row is further from the typical input configuration
    suspicion = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        suspicion.append((d, i))
    
    # Sort by suspicion (descending, as higher distance is more suspicious)
    suspicion.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [idx for _, idx in suspicion[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Found {len(suspicious_indices)} potentially mistyped records.")
    print("The following row indices are the most suspicious (most to least):")
    print(suspicious_indices[:10])
    
    if len(suspicious_indices) > 10:
        print("...")
