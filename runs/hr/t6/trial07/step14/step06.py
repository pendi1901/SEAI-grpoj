import ezr
import step01
import step05

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and 'reason' explains why based on the top drivers of attrition.
    """
    # Create a table to handle normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goal values for the input row using the median of the dataset
    # (or a more sophisticated approach if needed, but median is robust)
    row_filled = list(row)
    for i, val in enumerate(row_filled):
        if val == "?":
            row_filled[i] = ezr.mid(tbl.cols[i])
            
    # Calculate the distance of the input row from the ideal
    target_ydist = ezr.ydist(tbl, row_filled)
    
    # Calculate how many rows are worse (have a higher ydist) than this row
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    worse_count = sum(1 for d in all_ydists if d > target_ydist)
    p = worse_count / len(rows)
    
    # Get the top drivers of attrition to explain the ranking
    drivers = step05.blame(header, rows)
    
    # Construct a human-readable reason
    reason = (f"This arrangement ranks in the top {int(p*100)}% because its "
              f"{drivers[0]} and {drivers[1]} values align with our most "
              "stable, long-term employee profiles.")
    
    return p, reason

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row to justify (e.g., the 10th row)
    sample_row = list(rows[10])
    # Mask the goal columns
    for i, h in enumerate(header):
        if h.endswith(("+", "-")):
            sample_row[i] = "?"
            
    p, reason = justify(header, rows, sample_row)
    
    print(f"Ranking: {p:.2f}")
    print(f"Reason: {reason}")
