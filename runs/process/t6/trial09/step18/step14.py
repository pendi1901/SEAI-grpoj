import ezr
import step04

def flow(header, row, seen):
    """
    Warn the customer the moment a configuration starts to go bad.
    We define 'bad' as a significant drop in performance compared to 
    the historical trend. We use the logic from step04 to track 
    the best performance and flag if the current row is significantly 
    worse than the best seen so far.
    """
    # If we have no history, we cannot judge if it is 'bad'
    if not seen:
        return True
    
    # Create a table to calculate ydist
    # We use the current row and all seen rows to define the goal space
    data = [header] + seen + [row]
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for the new row and all previously seen rows
    current_ydist = ezr.ydist(tbl, row)
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If the new row is significantly worse than the best seen so far,
    # we return False (don't choose it) and implicitly warn the user.
    # We define 'bad' as being worse than the best by a margin 
    # (e.g., 2 standard deviations of the seen performance).
    best_seen = min(seen_ydists)
    
    # If the current row is worse than the best by a significant margin,
    # we flag it as 'bad'.
    if current_ydist > best_seen * 1.5:
        return False
    
    return True

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    # Simulate arrival of rows
    seen = []
    warnings = 0
    for row in rows:
        if not flow(header, row, seen):
            warnings += 1
        seen.append(row)
        
    print("Performance Monitoring Report:")
    print(f"Processed {len(rows)} configurations.")
    print(f"Number of performance warnings triggered: {warnings}")
    print("A warning is triggered when a new configuration performs significantly worse than the best seen so far.")
    
    exit(0)
