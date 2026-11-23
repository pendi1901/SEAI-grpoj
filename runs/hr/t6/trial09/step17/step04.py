import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'optimal' enough to trigger a retention 
    conversation immediately. We use the current 'seen' data to build a 
    model of what 'good' looks like.
    """
    # We need at least some data to make a decision
    if len(seen) < 10:
        return False
    
    # Create a table from seen data to calculate goals and distances
    tbl = ezr.Tbl([header] + seen)
    
    # A row is 'good' if its ydist is better (lower) than the median 
    # of what we have seen so far.
    ydists = [ezr.ydist(tbl, r) for r in seen]
    median_ydist = sorted(ydists)[len(ydists) // 2]
    
    # If the current row's distance to the goal is better than the median,
    # we flag it for a conversation.
    return ezr.ydist(tbl, row) < median_ydist

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    random.seed(12345)
    random.shuffle(rows)
    
    seen = []
    triggered = 0
    
    for row in rows:
        if flow(header, row, seen):
            triggered += 1
        seen.append(row)
        
    print(f"Processed {len(rows)} employee records.")
    print(f"Retention conversations triggered: {triggered}")
    print("Decision logic: Flagged employees whose performance metrics "
          "are better than the median of previously seen records.")
    
    exit(0)
