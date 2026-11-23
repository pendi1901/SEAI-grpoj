import ezr
import step09

def spot(header, rows):
    """
    Identify rows that contain input values far outside the range of what has been seen.
    We use the distance from the centroid of the input space (x-columns) as a measure
    of 'unusualness'. Rows with high xdist are those with settings far from the 
    average, which likely represent configurations never seen before.
    """
    # Create a table to leverage ezr's column and distance logic
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space (x-columns)
    mids = ezr.mids(tbl)
    
    # Calculate xdist for each row: how far the input configuration is from the average.
    # A high xdist indicates a row with settings that are 'unusual' or 'never seen'.
    scores = []
    for i, row in enumerate(rows):
        xd = ezr.xdist(tbl, row, mids)
        scores.append((xd, i))
    
    # Sort by xdist descending (most unusual first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in scores]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Get the suspicious indices
    suspects = spot(header, rows)
    
    print("Analysis of unusual configurations:")
    print(f"Identified {len(suspects)} rows that contain settings far outside the norm.")
    print("Top 5 most suspicious row indices (0-based):", suspects[:5])
    print("These rows represent configurations that are significantly different from the historical data.")
