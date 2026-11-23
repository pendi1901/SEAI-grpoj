import ezr
import step01

def spot(header, rows):
    """
    Identify rows containing input values that are 'out of distribution'
    compared to the rest of the dataset. We use the xdist (distance in 
    input space) to a centroid of the data to flag suspicious rows.
    """
    # Create a table to handle the data
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space (x columns)
    # ezr.mids(tbl) returns the median/mean for each column
    centroid = ezr.mids(tbl)
    
    # Calculate xdist for every row from the centroid
    # A row with a very high xdist is far from the "typical" configuration
    scored = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        scored.append((d, i))
    
    # Calculate mean and standard deviation of xdist to find outliers
    xdists = [s[0] for s in scored]
    mu = sum(xdists) / len(xdists)
    sd = (sum((x - mu)**2 for x in xdists) / len(xdists))**0.5
    
    # A row is suspicious if it is significantly far from the centroid
    # (e.g., more than 3 standard deviations away)
    threshold = mu + 3 * sd
    
    # Filter and sort by suspicion (highest xdist first)
    suspicious = [s for s in scored if s[0] > threshold]
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [s[1] for s in suspicious]

if __name__ == "__main__":
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    header = all_data[0]
    rows = all_data[1:]
    
    indices = spot(header, rows)
    
    print(f"Analysis complete. Found {len(indices)} rows with unusual settings.")
    if indices:
        print("The most suspicious rows (index, xdist from typical):")
        tbl = ezr.Tbl([header] + rows)
        centroid = ezr.mids(tbl)
        for idx in indices[:10]:
            dist = ezr.xdist(tbl, rows[idx], centroid)
            print(f"  Row {idx}: {dist:.4f}")
    else:
        print("No rows with unusual settings detected.")
    
    exit(0)
