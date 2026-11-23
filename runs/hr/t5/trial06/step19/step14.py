import ezr
import random

def flow(header, row, seen):
    """
    Detects if a team's composition has shifted significantly.
    We compare the current row's input distribution (xdist) to the 
    distribution of the 'seen' rows. If the current row is an outlier 
    (in the top 5% of distance from the centroid of seen rows), 
    we flag it as a shift in team dynamics.
    """
    if not seen:
        return False
    
    # Create a table to handle column definitions and distance calculations
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the centroid of the seen rows
    # We use the cached mids (middles) of the table
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of the current row from the centroid
    current_dist = ezr.xdist(tbl, row, centroid)
    
    # Calculate distances for all seen rows to establish a baseline
    seen_dists = [ezr.xdist(tbl, r, centroid) for r in seen]
    
    # A shift is detected if the current row is an outlier (top 5% of distance)
    # compared to the historical distribution of distances.
    threshold = sorted(seen_dists)[int(len(seen_dists) * 0.95)]
    
    return current_dist > threshold

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    shifts = 0
    
    for row in rows:
        if flow(header, row, seen):
            shifts += 1
        seen.append(row)
        
    print("Analysis: Detecting shifts in team composition.")
    print("-" * 60)
    print(f"Processed {len(rows)} employee records.")
    print(f"Detected {shifts} instances where the team composition")
    print("deviated significantly from historical norms.")
    print("-" * 60)
    print("Logic: A shift is flagged when a new employee's profile")
    print("is in the top 5% of distance from the team's average.")
