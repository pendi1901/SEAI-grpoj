import ezr
import step09

def flow(header, row, seen):
    """
    Detects if a team's composition has shifted significantly.
    We compare the incoming row to the distribution of 'seen' rows.
    If the row is an outlier (high xdist from the centroid of 'seen'),
    it suggests the team's profile is changing.
    """
    if len(seen) < 20:
        return False
    
    # Create a table of seen rows to establish the current team norm
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the centroid of the current team
    mids = ezr.mids(tbl)
    
    # Calculate how far the new row is from the current team norm
    d = ezr.xdist(tbl, row, mids)
    
    # Calculate the distribution of distances in the seen data
    # If the new row's distance is in the top 5% of historical distances,
    # it indicates a significant shift in team profile.
    seen_distances = [ezr.xdist(tbl, r, mids) for r in seen]
    threshold = sorted(seen_distances)[int(len(seen_distances) * 0.95)]
    
    return d > threshold

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    seen = []
    shifts = 0
    
    # Simulate monthly arrivals
    for row in rows:
        if flow(header, row, seen):
            shifts += 1
        seen.append(row)
    
    print("Team Composition Analysis: Detecting drift in team profile.")
    print(f"Processed {len(rows)} records.")
    print(f"Detected {shifts} instances where the team profile shifted significantly.")
    print("-" * 60)
    print("A shift is detected when an incoming employee record deviates")
    print("significantly from the established norm of the existing team.")
    
    exit(0)
