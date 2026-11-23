import ezr
import step01

def spot(header, rows):
    """
    Identify suspicious rows that might be 'failed runs'.
    We look for rows that are outliers in the input space (X-columns)
    relative to the rest of the data. Rows that are very far from 
    the centroid of the input space are flagged as suspicious.
    """
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the centroid of the input space
    # We use the cached mids from the table
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # A high xdist indicates the row is an outlier in input settings
    outliers = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        outliers.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    outliers.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in outliers[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    suspicious_indices = spot(header, rows)
    
    print("--- Analysis: Suspicious Rows ---")
    print(f"Identified {len(suspicious_indices)} rows that appear to be outliers.")
    print("These rows may represent failed runs or data entry errors.")
    print("Indices of the most suspicious rows (top 5):")
    for idx in suspicious_indices[:5]:
        print(f"Row {idx}: {rows[idx]}")
