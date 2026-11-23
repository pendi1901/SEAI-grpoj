import ezr
import step01

def spot(header, rows):
    """
    Identify rows that look like 'failed runs'.
    A failed run often results in extreme, outlier performance (very high ydist)
    or inconsistent behavior compared to the rest of the data.
    We identify these by calculating the ydist for every row and flagging
    those that are statistical outliers (e.g., > 3 standard deviations from the mean).
    """
    # Create a table to calculate ydist
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Calculate mean and standard deviation of ydist
    ydists = [s[0] for s in scored]
    mu = sum(ydists) / len(ydists)
    sd = (sum((x - mu)**2 for x in ydists) / len(ydists))**0.5
    
    # A row is suspicious if its ydist is significantly higher than the mean
    # (e.g., more than 2 standard deviations away)
    threshold = mu + 2 * sd
    
    # Filter and sort by suspicion (highest ydist first)
    suspicious = [s for s in scored if s[0] > threshold]
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [s[1] for s in suspicious]

if __name__ == "__main__":
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    header = all_data[0]
    rows = all_data[1:]
    
    indices = spot(header, rows)
    
    print(f"Analysis complete. Found {len(indices)} suspicious rows.")
    if indices:
        print("The most suspicious rows (index, ydist):")
        tbl = ezr.Tbl([header] + rows)
        for idx in indices[:10]:
            print(f"  Row {idx}: {ezr.ydist(tbl, rows[idx]):.4f}")
    else:
        print("No obviously failed runs detected.")
