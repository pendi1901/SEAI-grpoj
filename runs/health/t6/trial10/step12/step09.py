import ezr
import step01

def spot(header, rows):
    """
    Identify rows that are 'outliers' in the input space (x-columns).
    Rows that are very far from the rest of the data in x-space are 
    suspected of being mis-entered or failed runs.
    """
    # Create a table to handle column roles and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space (x-columns)
    # We use the cached mids from the table
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # A high xdist indicates the row is an outlier in the input space
    outliers = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        outliers.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    outliers.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in outliers[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    suspects = spot(header, rows)
    
    print(f"Analysis complete. Identified {len(suspects)} suspicious rows.")
    print("Most suspicious row indices (0-based):")
    print(suspects)
    
    print("\nDetails of the 3 most suspicious rows:")
    for i in suspects[:3]:
        print(f"Row {i}: {rows[i]}")
