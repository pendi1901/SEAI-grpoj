import ezr
import step03

def flow(header, row, seen):
    """
    Returns True if the current row is an outlier compared to the 'seen' 
    population, indicating the team no longer looks the way it normally does.
    We use the statistical 'same' test (cliffs and ks) on the ydist 
    distribution to detect a significant shift in team performance.
    """
    if len(seen) < 20:
        return False
    
    # Create a table for the seen population to define the "normal" state
    tbl_seen = ezr.Tbl([header] + seen)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl_seen, r) for r in seen]
    
    # Create a temporary table for the current row to calculate its ydist
    # We use the same column definitions as the seen table
    current_ydist = ezr.ydist(tbl_seen, row)
    
    # If the current row's performance (ydist) is significantly different 
    # from the distribution of the seen population, flag it.
    # We compare the current row against the distribution of the last 20 rows.
    recent_window = seen[-20:]
    recent_ydists = [ezr.ydist(tbl_seen, r) for r in recent_window]
    
    # If the current row is statistically different from the recent window,
    # it suggests the team's performance profile has shifted.
    # We use step03's certify (ezr.same) to check for significant difference.
    if not step03.certify([current_ydist], recent_ydists):
        return True
        
    return False

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
    
    print(f"Analysis: Monitoring team performance shifts.")
    print(f"Processed {len(rows)} employee records.")
    print(f"Detected {anomalies} instances where the team's performance profile")
    print("significantly deviated from recent trends.")
    print("-" * 40)
    print("Strategy: Flagged rows that are statistically different from the")
    print("recent performance distribution using cliffs and ks tests.")
