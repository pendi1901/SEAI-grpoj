import ezr
import random

def flow(header, row, seen):
    """
    Decide whether to accept a row immediately.
    We accept if the row is in the top 5% of the expected distribution
    based on the data seen so far.
    """
    # If this is the first row, we have no basis for comparison, so we wait.
    if not seen:
        return False
    
    # Create a table from the seen rows to establish a baseline
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the distance of the current row to the ideal
    # We use ydist which compares goals against their best possible values
    current_dist = ezr.ydist(tbl, row)
    
    # Calculate distances for all seen rows
    seen_dists = [ezr.ydist(tbl, r) for r in seen]
    
    # We define "top 5%" as being better than the 95th percentile of seen rows
    # (Lower ydist is better, so we look for values in the bottom 5%)
    seen_dists.sort()
    threshold_idx = max(0, int(len(seen_dists) * 0.05))
    threshold = seen_dists[threshold_idx]
    
    # Accept if the current row is better than our threshold
    return current_dist <= threshold

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Simulate arrival of rows one by one
    random.seed(1234567891)
    random.shuffle(all_rows)
    
    seen = []
    accepted = []
    
    for row in all_rows:
        if flow(header, row, seen):
            accepted.append(row)
            # Customer rule: "I cannot go back" and "stop"
            # We stop after the first acceptance as per the prompt's logic
            break
        seen.append(row)
        
    if accepted:
        print("Decision: Approved the incoming proposal.")
        print(f"Accepted row: {accepted[0]}")
    else:
        print("Decision: No suitable proposals were found in the stream.")
    
    exit(0)
