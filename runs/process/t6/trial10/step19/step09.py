import ezr
import step01

def spot(header, rows):
    """
    Identifies suspicious rows by calculating the distance of each row
    from the 'middle' of the dataset. Rows that are extreme outliers
    in the input space (x-columns) are flagged as suspicious.
    """
    # Create a table to handle column definitions and distance calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the centroid (mids) of the input columns
    # ezr.mids(tbl) returns a dict of the middle values for all columns
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # We use xdist to measure distance in the input space
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((d, i))
    
    # Sort by distance descending (most distant/suspicious first)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in distances[:limit]]

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    
    try:
        header = next(rows_gen)
        rows = list(rows_gen)
        
        suspicious_indices = spot(header, rows)
        
        print(f"Identified {len(suspicious_indices)} potentially mistyped or outlier records.")
        print("Most suspicious row indices (top 5):")
        for idx in suspicious_indices[:5]:
            print(f"Row {idx}: {rows[idx]}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
        
    exit(0)
