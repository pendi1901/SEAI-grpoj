import ezr
import random

def spot(header, rows):
    """
    Identify rows that are 'outliers' in the input space.
    Rows that are far from the center of the input distribution are 
    considered suspicious, as they may represent failed or invalid runs.
    """
    # Create a table to use ezr's distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space (mids)
    # mids() returns a dictionary of the median/mean for each column
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # We use xdist to measure distance in the input space (ignoring goals)
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((d, i))
    
    # Sort by distance descending: the furthest rows are the most suspicious
    distances.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the most suspicious rows
    return [item[1] for item in distances]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Identify suspicious rows
    suspects = spot(header, rows)
    
    print("Anomaly Detection: Identifying potentially failed/invalid runs.")
    print(f"Found {len(suspects)} rows. Top 5 most suspicious indices:")
    for i in range(min(5, len(suspects))):
        idx = suspects[i]
        # Calculate distance for context
        tbl = ezr.Tbl([header] + rows)
        dist = ezr.xdist(tbl, rows[idx], ezr.mids(tbl))
        print(f" - Row {idx}: Distance from centroid = {dist:.4f}")
    
    print("\nThese rows are the furthest from the typical input configurations "
          "and may represent failed or erroneous experimental runs.")
    exit(0)
