import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is worth a 'what would keep you here' conversation.
    We use the 'seen' rows to build a model of what 'good' looks like.
    If the current row is significantly better than the average of what we've seen,
    we flag it (return True).
    """
    # We need at least a small sample to establish a baseline
    if len(seen) < 20:
        return False
    
    # Create a table from the history to understand the goal space
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the distance of the current row to the ideal goals
    # A lower ydist means the employee is closer to the 'best' outcomes
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate the average ydist of the rows we have seen so far
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    avg_ydist = sum(seen_ydists) / len(seen_ydists)
    
    # If the current row is better (lower distance to ideal) than the average,
    # flag it for a conversation. We use a threshold to be selective.
    # Here, we flag if the row is in the top 20% of what we've seen.
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.2)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival of rows one by one
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    flagged_count = 0
    
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
        
    print(f"Processed {len(rows)} employee records.")
    print(f"Flagged {flagged_count} employees for 'what would keep you here' conversations.")
    print("Decision logic: Flagged employees whose goal metrics are in the top 20% of historical data.")
