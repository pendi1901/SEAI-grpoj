import ezr
import step01

def spot(header, rows):
    """
    Identify suspicious rows. A row is suspicious if it is an outlier in the 
    input space (x-columns) relative to the rest of the data. We use the 
    xdist from the centroid of all rows to find rows that are 'far' from 
    the typical configuration.
    """
    # Create a table to handle column roles and distance calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the centroid (mids) of the entire dataset
    centroid = ezr.mids(tbl)
    
    # Calculate xdist for each row from the centroid
    # Rows with high xdist are outliers in the input configuration space
    scored = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        scored.append((d, i))
    
    # Sort by distance descending (most suspicious/outlier first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
        
        suspicious_indices = spot(header, rows)
        
        print(f"Analysis complete. Found {len(suspicious_indices)} suspicious configurations.")
        print("Indices of the most suspicious rows (most suspicious first):")
        print(suspicious_indices)
        
        print("\nTop 3 most suspicious configurations:")
        for i in suspicious_indices[:3]:
            print(f"Row {i}: {rows[i]}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
        
    exit(0)
