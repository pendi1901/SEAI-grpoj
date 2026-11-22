import ezr
import random

def flow(header, row, seen):
    """
    Decide whether to approve a row on the spot.
    We approve if the row is significantly better than the average 
    of what we have seen so far.
    """
    if not seen:
        return True
    
    # Create a table to handle column logic and normalization
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the ydist of the current row
    # Note: Since goals are in the row, we can calculate ydist directly
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate the average ydist of seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    avg_ydist = sum(seen_ydists) / len(seen_ydists)
    
    # If the current row is better (lower ydist) than the average, approve it.
    # We use a small buffer to be slightly more selective.
    return current_ydist < (avg_ydist * 0.95)

if __name__ == "__main__":
    # Load data
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
    print(f"Approved {len(approved)} proposals.")
    
    if approved:
        # Calculate average performance of approved vs total
        tbl = ezr.Tbl([header] + rows)
        avg_all = sum(ezr.ydist(tbl, r) for r in rows) / len(rows)
        avg_app = sum(ezr.ydist(tbl, r) for r in approved) / len(approved)
        
        print(f"Average ydist of all proposals: {avg_all:.4f}")
        print(f"Average ydist of approved proposals: {avg_app:.4f}")
        print("Strategy: Approved proposals that performed better than the running average.")
