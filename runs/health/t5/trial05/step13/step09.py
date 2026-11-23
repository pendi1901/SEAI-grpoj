import ezr

def spot(header, rows):
    """
    Finds suspicious rows (outliers) by calculating the distance of each row
    from the centroid of the entire dataset. Rows with an unusually high 
    xdist (distance in input space) are flagged as potential errors.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space
    # ezr.mids(tbl) returns a dictionary of column indices to their median/mean
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # We use xdist because we are looking for suspicious input configurations
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((i, d))
    
    # Sort by distance descending (most suspicious first)
    distances.sort(key=lambda x: x[1], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[0] for item in distances[:10]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    suspicious_indices = spot(header, rows)
    
    print("--- Analysis: Suspicious Rows ---")
    print("The following rows have input configurations that deviate significantly")
    print("from the rest of the dataset, suggesting potential data entry errors:")
    
    for i, idx in enumerate(suspicious_indices, 1):
        print(f"{i}. Row index {idx} (Distance from centroid: {ezr.xdist(ezr.Tbl([header]+rows), rows[idx], ezr.mids(ezr.Tbl([header]+rows))):.4f})")
    
    print("\nThese rows should be reviewed for data quality issues.")
