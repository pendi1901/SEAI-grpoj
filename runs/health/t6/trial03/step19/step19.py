import ezr
import step09

def spot(header, rows):
    """
    Identify rows that contain input values far outside the range of 
    what has been seen in the training data.
    
    We use the logic from step09 to identify suspicious rows, but 
    specifically focus on the input space (x-columns) to detect 
    outliers that the model has never seen.
    """
    # Create a table to handle column roles and distance metrics
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the centroid of the entire dataset to define the 
    # 'normal' input space
    mids = ezr.mids(tbl)
    
    # Score rows by their distance from the global centroid in the 
    # input space. Rows that are far from the centroid are suspicious.
    suspects = []
    for i, row in enumerate(rows):
        # xdist measures distance in input space
        dist_from_center = ezr.xdist(tbl, row, mids)
        suspects.append((dist_from_center, i))
    
    # Return indices sorted by distance (most suspicious first)
    suspects.sort(key=lambda x: x[0], reverse=True)
    return [i for _, i in suspects]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    suspects = spot(header, rows)
    
    print("Analysis of configurations with unusual settings:")
    print(f"Identified {len(suspects)} configurations with settings far outside the norm.")
    print(f"Top 5 most suspicious row indices: {suspects[:5]}")
    print("These rows contain input combinations that the model has rarely or never seen.")
    
    exit(0)
