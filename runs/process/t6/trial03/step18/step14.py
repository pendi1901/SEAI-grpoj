import ezr
import step01
import step03

def flow(header, row, seen):
    """
    Warn the customer if the incoming row is significantly worse than 
    the established performance baseline.
    
    We define 'bad' as a row whose ydist is statistically significantly 
    worse (higher) than the distribution of the 'seen' rows.
    """
    if len(seen) < 30:
        return False
    
    # Create a table of seen rows to establish a baseline
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Calculate ydist for the current row
    # We use the same table to normalize the current row
    current_ydist = ezr.ydist(tbl, row)
    
    # If the current row's ydist is significantly higher than the 
    # distribution of seen rows, it's a warning sign.
    # We use the statistical test from step03 (cliffs/ks) to check 
    # if the current row is an outlier on the 'bad' side.
    # Here we check if the current row is worse than the 90th percentile of seen.
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.9)]
    
    return current_ydist > threshold

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    seen = []
    warnings = 0
    
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            warnings += 1
            # Only print the first few warnings to avoid flooding the console
            if warnings <= 5:
                print(f"Warning: Row {i} shows degraded performance.")
        seen.append(row)
        
    print(f"Monitoring complete.")
    print(f"Total rows processed: {len(rows)}")
    print(f"Total performance warnings triggered: {warnings}")
