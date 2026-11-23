import ezr
import random

def flow(header, row, seen):
    """
    Warn the customer if a newly arrived row is significantly worse than
    the historical performance baseline. We define 'going bad' as the 
    current row's performance (ydist) being significantly worse than the 
    95th percentile of performance observed in the 'seen' history.
    """
    if len(seen) < 10:
        return False
    
    # Create a table to handle normalization and ydist calculations
    # We use the 'seen' rows to establish the performance baseline
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for all seen rows
    # Lower ydist is better.
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Calculate ydist for the current row
    # If the row has '?', ydist handles it via normalization
    current_ydist = ezr.ydist(tbl, row)
    
    # Threshold: Is this row performing worse than 95% of what we have seen?
    # We use the 95th percentile of seen rows as our 'bad performance' threshold.
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.95)]
    
    # If the current row's ydist is higher than the threshold, it is 'going bad'
    return current_ydist > threshold

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    warnings = 0
    
    for row in rows:
        if flow(header, row, seen):
            warnings += 1
        seen.append(row)
        
    print("Analysis: Monitoring project performance week by week.")
    print(f"Processed {len(rows)} incoming project configurations.")
    print(f"Detected {warnings} instances where a configuration started to 'go bad'.")
    print("A warning is triggered when a new configuration's performance (ydist) ")
    print("falls into the bottom 5% of historical performance.")
    
    exit(0)
