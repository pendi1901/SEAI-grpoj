import ezr
import random

def flow(header, row, seen):
    """
    Warn the customer if the incoming row is 'bad'.
    We define 'bad' as a row that is significantly worse than the 
    historical performance baseline. We use the 95th percentile of 
    the 'seen' rows as a threshold for 'good' performance. If the 
    new row's ydist is significantly higher than this threshold, 
    we flag it as a potential warning (returning True).
    """
    if not seen:
        return False
    
    # Create a table to handle normalization and ydist calculations
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    seen_ydists.sort()
    
    # Define the threshold for 'bad' performance.
    # We use the 95th percentile of seen performance.
    # If the new row is worse than this, it's a warning.
    threshold = seen_ydists[int(len(seen_ydists) * 0.95)]
    
    # Calculate ydist for the new row
    current_ydist = ezr.ydist(tbl, row)
    
    # Return True if the row is significantly worse than the threshold
    return current_ydist > threshold

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    warnings = 0
    
    # Simulate arrival of rows one by one
    for row in rows:
        if flow(header, row, seen):
            warnings += 1
        seen.append(row)
    
    print("Analysis: Monitoring project performance week by week.")
    print(f"Processed {len(rows)} incoming configurations.")
    print(f"Warnings triggered: {warnings}")
    print("A warning is triggered when a new configuration performs significantly")
    print("worse than the 95th percentile of all previously seen configurations.")
