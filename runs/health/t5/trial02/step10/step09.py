import ezr
import random

def spot(header, rows):
    """
    Identify rows that are 'suspicious' (outliers in the input space).
    Rows that are very far from the rest of the data in the input space
    are likely to be failed runs or data entry errors.
    """
    # Create a table to handle column roles and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space
    # We use the cached mids from the table
    mids = ezr.mids(tbl)
    
    # Calculate xdist for every row from the centroid
    # Rows with high xdist are outliers
    scores = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, mids)
        scores.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Identified {len(suspicious_indices)} suspicious rows.")
    print("Most suspicious row indices (0-based):")
    print(suspicious_indices[:10])
    
    if suspicious_indices:
        print("\nDetails of the most suspicious row:")
        idx = suspicious_indices[0]
        for h, v in zip(header, rows[idx]):
            print(f"  {h}: {v}")
