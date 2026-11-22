import ezr
import random

def flow(header, row, seen):
    """
    Decide whether to approve a row on the spot.
    We compare the current row's potential against the 'seen' data.
    If the row is in the top 5% of the distribution of 'seen' rows,
    we approve it.
    """
    if not seen:
        return False
    
    # Create a table from seen rows to calculate ydist
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Calculate ydist for the new row
    # Note: We must treat the new row as having its goals known 
    # to evaluate its quality against the historical context.
    current_ydist = ezr.ydist(tbl, row)
    
    # We approve if the current row is better than 95% of what we have seen
    # (i.e., its ydist is in the bottom 5% of seen ydist values)
    threshold = sorted(seen_ydists)[max(0, int(len(seen_ydists) * 0.05))]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    approved = []
    
    for row in rows:
        if flow(header, row, seen):
            approved.append(row)
        seen.append(row)
        
    print(f"Processed {len(rows)} proposals.")
    print(f"Approved {len(approved)} proposals based on real-time evaluation.")
    
    if approved:
        goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
        print("\nSample of approved rows (Goal columns: Cost-, Score-, Idle-):")
        for row in approved[:5]:
            goals = [row[i] for i in goal_indices]
            print(f"Goals: {goals}")
