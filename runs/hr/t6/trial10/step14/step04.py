import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is a 'retention risk' candidate.
    We use the 'acquire' logic: if the row is closer to the 'best' 
    rows seen so far than the 'rest', it is a high-value employee 
    worth keeping.
    """
    if not seen:
        return False
    
    # Build a table from the history to establish the 'best' vs 'rest'
    # We use the existing rows to define the current landscape
    tbl = ezr.Tbl([header] + seen)
    
    # We need to evaluate the current row against the existing population.
    # A row is a candidate for a 'stay' conversation if it is 
    # significantly better than the average employee (low ydist).
    # We define 'better' as being in the top 10% of the current distribution.
    
    # Calculate ydist for all seen rows
    scores = [ezr.ydist(tbl, r) for r in seen]
    threshold = sorted(scores)[max(0, int(len(scores) * 0.1))]
    
    # If the current row's potential ydist is better than the 10th percentile,
    # flag it for a conversation.
    current_ydist = ezr.ydist(tbl, row)
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    flagged_count = 0
    
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
        
    print(f"Processed {len(rows)} employee reviews.")
    print(f"Flagged {flagged_count} employees for 'what would keep you here' conversations.")
    print("Logic: Flagged employees are those in the top 10% of tenure/management alignment.")
