import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is worth a 'what would keep you here' conversation.
    We compare the current row against the 'seen' population using the 
    distance-to-ideal (ydist) metric. If the row is in the top 5% of 
    performance/tenure potential, we flag it.
    """
    if not seen:
        return False
    
    # Create a table from seen rows to establish the context of 'good'
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for the current row
    # Note: row might have '?' for goals, but ydist handles normalization
    # We need to estimate the goals if they are missing.
    # For simplicity, we use the median of the seen data to fill '?'
    current_row = list(row)
    for i, val in enumerate(current_row):
        if val == "?":
            current_row[i] = ezr.mid(tbl.cols[i])
            
    current_ydist = ezr.ydist(tbl, current_row)
    
    # Compare against the distribution of seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If this row is better (lower ydist) than 95% of what we've seen,
    # it's a priority for a retention conversation.
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Simulate arrival
    random.seed(1234567891)
    random.shuffle(all_rows)
    
    seen = []
    flags = 0
    for row in all_rows:
        # Mask goals for the decision process
        masked_row = list(row)
        for i, h in enumerate(header):
            if h.endswith(("+", "-")):
                masked_row[i] = "?"
        
        if flow(header, masked_row, seen):
            flags += 1
        
        seen.append(row)
        
    print(f"Processed {len(all_rows)} employee records.")
    print(f"Identified {flags} employees for 'what would keep you here' conversations.")
    print("Decision logic: Flagged top 5% of potential based on historical performance.")
