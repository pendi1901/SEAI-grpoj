import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the potential
    search space, estimated from the rows seen so far.
    """
    # If we haven't seen enough to estimate a distribution, keep looking
    if len(seen) < 20:
        return False

    # Create a temporary table to calculate ydist
    # We use the current row and the seen rows to establish the context
    data = [header] + seen + [row]
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for the current row
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # We stop if the current row is better than 95% of what we've seen
    # (i.e., it is in the top 5% of the current distribution)
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    found_idx = -1
    
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_idx = i
            break
        seen.append(row)
        
    if found_idx != -1:
        print(f"Stopped at row {found_idx + 1}: Found a configuration good enough to ship.")
    else:
        print("Processed all rows without finding a configuration meeting the threshold.")
