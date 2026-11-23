import ezr
import step09

def flow(header, row, seen):
    """
    Decide if the current row is 'suspicious' (an outlier) compared to the 
    population of rows seen so far. If the row is significantly different 
    from the historical centroid, return True.
    """
    if len(seen) < 20:
        return False
    
    # Create a table from the seen rows to establish the current 'normal'
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the centroid of the seen data
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of the new row from the current centroid
    # We use xdist to measure deviation in input space
    current_dist = ezr.xdist(tbl, row, centroid)
    
    # Calculate the distribution of distances seen so far
    seen_dists = [ezr.xdist(tbl, r, centroid) for r in seen]
    
    # If the current row's distance is in the top 5% of deviations, 
    # it is an anomaly (the team no longer looks the way it normally does).
    threshold = sorted(seen_dists)[int(len(seen_dists) * 0.95)]
    
    return current_dist > threshold

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    seen = []
    anomalies = 0
    
    for row in all_rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print(f"Analysis: Monitoring team composition over {len(all_rows)} records.")
    print(f"Detected {anomalies} instances where the team structure deviated significantly from the norm.")
    print("Anomalies are identified as records that fall into the top 5% of input-space outliers.")
