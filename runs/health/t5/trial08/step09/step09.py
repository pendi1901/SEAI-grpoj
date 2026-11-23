import ezr

def spot(header, rows):
    """
    Identifies suspicious rows (outliers) that might represent failed runs.
    We define 'suspicious' as rows that have an unusually high distance 
    from the rest of the data in the input space (x-columns).
    """
    # Create a table to handle column metadata and normalization
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space (x-columns)
    # The centroid is the 'mid' of each column
    centroid = {col.at: ezr.mid(col) for col in tbl.x}
    
    # Calculate the distance of each row from the centroid
    # Rows that are very far from the centroid are likely outliers
    scores = []
    for i, row in enumerate(rows):
        # xdist calculates the distance between a row and a set of values (mids)
        d = ezr.xdist(tbl, row, centroid)
        scores.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Customer Query: Some result rows look like a run that failed and got written down anyway. Find them.")
    print(f"Analysis: Identified {len(suspicious_indices)} potentially failed/outlier configurations.")
    print(f"Top 5 most suspicious row indices: {suspicious_indices[:5]}")
    
    if suspicious_indices:
        print("\nSample of the most suspicious row:")
        print(f"Row {suspicious_indices[0]}: {rows[suspicious_indices[0]]}")
        print("These rows are statistically distant from the central tendency of the input settings.")
    
    exit(0)
