import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is worth a 'retention' conversation.
    We compare the current row against the 'seen' population.
    If the row is in the top 5% of the current distribution (based on ydist),
    we flag it for a conversation (True).
    """
    if not seen:
        return False
    
    # Build a table from the seen data to calculate the current distribution
    # We use the header to ensure goals (+/-) are correctly identified
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate how far the current row is from the ideal goals
    # ydist returns 0 for perfect, higher for worse
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate the ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If the current row is better than 95% of what we have seen, 
    # it is a high-retention-risk/high-value candidate.
    # We define "better" as having a lower ydist (closer to ideal).
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    seen = []
    decisions = 0
    for row in rows:
        if flow(header, row, seen):
            decisions += 1
        seen.append(row)
    
    print(f"Processed {len(rows)} employee records.")
    print(f"Flagged {decisions} employees for a 'what would keep you here' conversation.")
    print("Strategy: Flagged employees in the top 5% of retention-goal performance.")
