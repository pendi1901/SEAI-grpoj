import ezr
import random

def flow(header, row, seen):
    """
    Detects if the current team (represented by 'row') is an outlier compared 
    to the historical 'seen' data. We use the distance from the centroid of 
    the 'seen' data to determine if the current team's configuration is 
    statistically unusual.
    """
    if len(seen) < 30:
        return False  # Need a baseline to define 'normal'
    
    # Create a table from the history to understand the 'normal' space
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the centroid of the historical data
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of the current row from the historical centroid
    # xdist measures distance over input columns
    current_dist = ezr.xdist(tbl, row, centroid)
    
    # Calculate distances for all seen rows to establish a distribution
    seen_dists = [ezr.xdist(tbl, r, centroid) for r in seen]
    
    # Define 'not normal' as being in the top 5% of distance (outliers)
    # This indicates the team configuration is significantly different from the norm
    threshold = sorted(seen_dists)[int(len(seen_dists) * 0.95)]
    
    return current_dist > threshold

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival of teams one by one
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    anomalies = 0
    
    print("Monitoring team configurations for anomalies...")
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print(f"Total teams reviewed: {len(rows)}")
    print(f"Teams flagged as 'not looking normal': {anomalies}")
    print("Decision logic: Flagged teams in the top 5% of distance from the historical centroid.")
