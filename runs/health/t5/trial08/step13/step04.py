import ezr

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    distribution of ydist, based on the history seen so far.
    """
    # Create a table to handle column metadata and normalization
    data = [header] + seen + [row]
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all seen rows
    # A lower ydist is better (closer to goals)
    scores = [ezr.ydist(tbl, r) for r in seen]
    
    # If we haven't seen enough to establish a baseline, keep looking
    if len(scores) < 20:
        return False
    
    # Current row's score
    current_score = ezr.ydist(tbl, row)
    
    # Threshold: Is this row better than 95% of what we've seen?
    # We sort scores to find the 5th percentile
    scores.sort()
    threshold = scores[int(len(scores) * 0.05)]
    
    return current_score <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    seen = []
    found_idx = -1
    
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_idx = i
            break
        seen.append(row)
    
    if found_idx != -1:
        print(f"Stopped at row {found_idx + 1}: Found a setup good enough to ship.")
        print(f"Row data: {rows[found_idx]}")
    else:
        print("Processed all rows without finding a setup meeting the criteria.")
    
    exit(0)
