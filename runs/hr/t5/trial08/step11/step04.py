import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is worth a 'retention' conversation.
    We use the 'seen' rows to build a model of what 'good' looks like
    (using the ydist metric) and compare the current row against that.
    If we have enough data, we pick the top 5% of candidates.
    """
    # Need at least some history to make a relative decision
    if len(seen) < 20:
        return False
    
    # Create a table from seen rows to calculate ydist
    # We filter out rows that might have missing goals if necessary
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for the current row
    # ydist measures how far a row is from the ideal goal values
    # Lower ydist is better
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If the current row is in the top 5% of what we have seen so far,
    # flag it for a conversation.
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    # Load the data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    selected_count = 0
    
    print("Processing employee reviews one by one...")
    for row in rows:
        if flow(header, row, seen):
            selected_count += 1
        seen.append(row)
        
    print(f"Total employees reviewed: {len(rows)}")
    print(f"Employees flagged for retention conversation: {selected_count}")
    print("Decision logic: Flagged top 5% of arrivals based on tenure/retention goals.")
    
    exit(0)
