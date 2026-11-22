import ezr
import step09

def spot(header, rows):
    """
    Identify rows that are 'out of distribution' (OOD) compared to the 
    training data. We use xdist to measure how far a row's input 
    configuration is from the global centroid of all rows. Rows with 
    an xdist significantly higher than the average are flagged as 
    suspicious (i.e., settings we have never seen).
    """
    tbl = ezr.Tbl([header] + rows)
    mids = ezr.mids(tbl)
    
    # Calculate xdist for each row
    # High xdist indicates a configuration far from the typical data
    scores = []
    for i, row in enumerate(rows):
        x_d = ezr.xdist(tbl, row, mids)
        scores.append((x_d, i))
    
    # Sort by xdist descending (most unusual first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of the top 5% most unusual rows
    limit = max(1, len(rows) // 20)
    return [x[1] for x in scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    suspicious_indices = spot(header, rows)
    
    print(f"Identified {len(suspicious_indices)} rows with settings far outside typical ranges.")
    print("Indices of the most suspicious rows (most unusual first):")
    print(suspicious_indices)
    
    print("\nDetails of the top 3 most unusual rows:")
    for idx in suspicious_indices[:3]:
        print(f"Row {idx}: {rows[idx]}")
