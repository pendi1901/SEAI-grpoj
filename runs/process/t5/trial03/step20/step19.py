import ezr
import random

def spot(header, rows):
    """
    Identify rows that are 'suspicious' by checking if they are outliers
    in the input space. We use the distance to the centroid of the 
    input columns as a measure of suspicion.
    """
    # Create a table to handle column definitions and normalization
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space
    # We use the cached mids from the table
    mids = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # A row is suspicious if it is far from the 'typical' input configuration
    suspicion_scores = []
    for i, row in enumerate(rows):
        # xdist calculates the distance over input columns only
        d = ezr.xdist(tbl, row, mids)
        suspicion_scores.append((d, i))
    
    # Sort by suspicion (distance) descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in suspicion_scores[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis: Found {len(suspicious_indices)} setups that are unlike anything we have seen.")
    print("These configurations are outliers in our input space and may be errors.")
    print("The most suspicious row indices (most suspicious first):")
    print(suspicious_indices)
    
    # Show a sample of why they might be suspicious
    print("\nSample of suspicious rows (first 3):")
    for idx in suspicious_indices[:3]:
        row = rows[idx]
        # Show a few input columns to illustrate
        sample_inputs = {header[i]: row[i] for i in range(min(4, len(header)))}
        print(f"Row {idx}: {sample_inputs}")
