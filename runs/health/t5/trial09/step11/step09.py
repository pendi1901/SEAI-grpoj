import ezr
import random

def spot(header, rows):
    """
    Find suspicious rows that might be 'failed runs'.
    We look for rows that are outliers in the input space (x-columns)
    relative to the rest of the data. Rows that are far from the 
    centroid of the input space are flagged as suspicious.
    """
    # Create a table to handle column roles
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid (mids) of the input space
    # We use the cached mids from the table
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid in the x-space
    # A high xdist indicates the row is an outlier in input parameters
    scores = []
    for i, row in enumerate(rows):
        dist = ezr.xdist(tbl, row, centroid)
        scores.append((i, dist))
    
    # Sort by distance descending (most suspicious/outlier first)
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return the indices of the rows
    return [item[0] for item in scores]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    # Print the top 5 most suspicious rows
    print("Analysis complete.")
    print("The following rows are identified as potential 'failed runs' (outliers in input space):")
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f" - Row {idx}: {rows[idx]}")
        
    exit(0)
