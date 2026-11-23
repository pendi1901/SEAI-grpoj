import ezr
import step01

def spot(header, rows):
    """
    Identify suspicious rows by finding outliers.
    We use the distance from the centroid (mids) of the data as a measure
    of how much a row deviates from the typical configuration.
    """
    # Create a table to calculate column statistics
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid (mids) of the data
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # Higher distance means the row is more "unusual" or "mistyped"
    scores = []
    for i, row in enumerate(rows):
        # xdist calculates distance based on input columns
        d = ezr.xdist(tbl, row, centroid)
        scores.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis: Found {len(suspicious_indices)} potentially mistyped records.")
    print("The following row indices are the most suspicious (most to least):")
    print(suspicious_indices)
    
    if suspicious_indices:
        print("\nSample of suspicious row data:")
        for i in suspicious_indices[:3]:
            print(f"Row {i}: {rows[i]}")
    
    exit(0)
