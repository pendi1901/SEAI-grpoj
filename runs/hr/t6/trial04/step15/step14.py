import ezr
import step03

def flow(header, row, seen):
    """
    Detects if a team's performance distribution has shifted significantly.
    We compare the current row's ydist against the distribution of ydist
    values in 'seen'. If the current row is a statistical outlier compared
    to the 'seen' population (using the same logic as step03), we flag it.
    """
    if len(seen) < 30:
        return False
    
    tbl = ezr.Tbl([header] + seen)
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Current row ydist
    current_ydist = ezr.ydist(tbl, row)
    
    # Check if the current row's ydist is statistically different from the 
    # distribution of seen ydist values.
    # We use step03's certify (which uses ezr.same) to check for drift.
    # If they are NOT the same (not noise), we flag the row as a shift.
    return not step03.certify(seen_ydists, [current_ydist])

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    seen = []
    shifts = 0
    for row in rows:
        if flow(header, row, seen):
            shifts += 1
        seen.append(row)
    
    print(f"Processed {len(rows)} employee records.")
    print(f"Detected {shifts} instances where the team's performance metrics "
          "shifted significantly from historical norms.")
    print("Logic: A shift is detected when a new record's goal-distance is "
          "statistically distinguishable from the distribution of previous records.")
