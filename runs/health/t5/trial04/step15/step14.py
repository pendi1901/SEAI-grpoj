import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    performance distribution based on the history of rows seen so far.
    """
    # If we haven't seen enough to establish a baseline, keep looking
    if len(seen) < 20:
        return False

    # Create a table from the history to calculate the ideal goal values
    # We need to handle the fact that 'seen' rows are complete
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the ydist of the current row relative to the history
    # ydist measures distance to the ideal (0 is best)
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows to establish a threshold
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # We stop if the current row is in the top 5% of what we've seen
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Optimization stopped at row {i+1} (out of {len(rows)}).")
            print(f"The configuration at this row is in the top 5% of performance seen so far.")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("No row met the criteria; processed all records.")
    
    exit(0)
