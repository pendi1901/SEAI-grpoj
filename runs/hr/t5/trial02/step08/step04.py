import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is a 'keeper' (needs a retention conversation).
    We use a simple heuristic: if the row is significantly better than the 
    average of what we have seen so far, we flag it.
    """
    if not seen:
        return True
    
    # Create a temporary table to calculate ydist
    # We need to handle the fact that 'seen' might contain rows with '?'
    # but ezr.ydist works on the goals.
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the ydist of the current row
    # If the row has '?' in goal columns, we treat it as neutral
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate the average ydist of seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    avg_ydist = sum(seen_ydists) / len(seen_ydists)
    
    # If the current row is better (lower ydist) than the average,
    # we flag it for a retention conversation.
    # We use a small buffer to avoid flagging everything.
    return current_ydist < (avg_ydist * 0.9)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival of rows
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    flagged_count = 0
    
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
        
    print(f"Processed {len(rows)} employee records.")
    print(f"Flagged {flagged_count} employees for a 'what would keep you here' conversation.")
    print("Strategy: Flagging employees whose performance/retention metrics are better than the historical average.")
    
    exit(0)
