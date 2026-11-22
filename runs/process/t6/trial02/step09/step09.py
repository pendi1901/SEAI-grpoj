import ezr
import step01

def spot(header, rows):
    """
    Identify rows that do not fit the distribution of the data.
    We use the distance from the centroid of the input (X) columns
    as a measure of 'suspicion'. Rows that are far from the 
    center of the input space are considered outliers.
    """
    # Create a table to handle column definitions and distance calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the centroid of the input space (the 'mids' of X columns)
    # ezr.mids(tbl) returns a dict of {at: mid_value}
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # Higher distance = more suspicious
    suspicions = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        suspicions.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    suspicions.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows
    return [item[1] for item in suspicions]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Get suspicious indices
    suspicious_indices = spot(header, rows)
    
    print("Anomaly Detection: Rows that do not fit the input distribution.")
    print(f"Found {len(suspicious_indices)} rows. Top 5 most suspicious:")
    print("-" * 40)
    
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"Row {idx} is highly suspicious (outlier in input space).")
        
    exit(0)
