import ezr
import step01

def spot(header, rows):
    """
    Identify suspicious rows. A row is suspicious if its input values
    are outliers compared to the rest of the dataset. We use the 
    distance from the centroid of the input space (xdist) as a measure 
    of how 'unusual' a row is.
    """
    # Create a table to handle column statistics
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the centroid of the input space
    # ezr.mids(tbl) returns a dictionary of column middles
    centroid = ezr.mids(tbl)
    
    # Calculate xdist for every row from the centroid
    # Higher xdist means the row is further from the 'typical' configuration
    suspicious = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        suspicious.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, int(len(rows) * 0.05))
    return [idx for _, idx in suspicious[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    suspect_indices = spot(header, rows)
    
    print("Anomaly Detection Report:")
    print(f"Identified {len(suspect_indices)} potentially mistyped configurations.")
    print(f"{'Rank':<10} | {'Row Index':<10}")
    print("-" * 25)
    
    for rank, idx in enumerate(suspect_indices[:10]):
        print(f"{rank+1:<10} | {idx:<10}")
        
    exit(0)
