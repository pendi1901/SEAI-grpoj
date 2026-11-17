import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is a 'high-value' employee worth retaining.
    We use a simple threshold based on the 'YearsAtCompany+' and 
    'YearsInCurrentRole+' goals. If the row is in the top 5% of 
    tenure compared to what we have seen so far, we flag it.
    """
    # Identify indices for the goal columns
    idx_years_at = header.index("YearsAtCompany+")
    idx_years_role = header.index("YearsInCurrentRole+")
    
    # If we haven't seen enough, keep looking
    if len(seen) < 10:
        return False
    
    # Calculate score for current row
    val1 = row[idx_years_at] if row[idx_years_at] != "?" else 0
    val2 = row[idx_years_role] if row[idx_years_role] != "?" else 0
    score = val1 + val2
    
    # Calculate scores of seen rows
    seen_scores = []
    for s in seen:
        v1 = s[idx_years_at] if s[idx_years_at] != "?" else 0
        v2 = s[idx_years_role] if s[idx_years_role] != "?" else 0
        seen_scores.append(v1 + v2)
    
    # If this row is in the top 5% of what we've seen, flag it
    threshold = sorted(seen_scores, reverse=True)[int(len(seen_scores) * 0.05)]
    return score >= threshold

if __name__ == "__main__":
    # Load the data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival of rows one at a time
    seen = []
    flagged_count = 0
    
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
    
    print(f"Analyzed {len(rows)} employee records arriving one by one.")
    print(f"Flagged {flagged_count} employees for a 'what would keep you here' conversation.")
    print("Decision logic: Flagged employees in the top 5% of tenure based on historical arrivals.")
    exit(0)
