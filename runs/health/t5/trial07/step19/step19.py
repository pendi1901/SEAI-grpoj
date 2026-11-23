import ezr
import random

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' because they contain input values
    that are far from the observed distribution (outliers in X-space).
    Returns the indices of the rows, most suspicious first.
    """
    # Create a table to handle column roles and distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # We use the centroid of the input space (mids) to identify outliers.
    # Rows that are far from the centroid in X-space are considered suspicious.
    mids = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid in X-space.
    # A high xdist indicates the row is an outlier compared to the rest.
    suspicious = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, mids)
        suspicious.append((d, i))
    
    # Sort by distance descending (most distant/suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the most suspicious rows
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying configurations with unusual input settings.")
    print("The following rows contain input values that are significantly different")
    print("from the rest of the dataset, suggesting potential data entry errors:")
    
    # Print the top 5 most suspicious rows
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"{i+1}. Row {idx}: {rows[idx]}")
    
    print(f"\nTotal suspicious rows identified: {len(suspicious_indices)}")
    exit(0)
