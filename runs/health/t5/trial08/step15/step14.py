import ezr

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 1% of the expected 
    distribution of ydist, based on the history seen so far.
    """
    # If we haven't seen enough to establish a baseline, keep looking
    if len(seen) < 50:
        return False
    
    # Create a table to handle column metadata and normalization
    # We include 'seen' to establish the context of the performance distribution
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for all seen rows
    # A lower ydist is better (closer to goals)
    scores = [ezr.ydist(tbl, r) for r in seen]
    
    # Current row's score
    current_score = ezr.ydist(tbl, row)
    
    # Threshold: Is this row better than 99% of what we've seen?
    # We sort scores to find the 1st percentile (the "best of the best")
    scores.sort()
    threshold = scores[int(len(scores) * 0.01)]
    
    # If the current row is better than the 1st percentile, stop
    return current_score <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    seen = []
    found_idx = -1
    
    # Simulate the arrival of rows one by one
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_idx = i
            break
        seen.append(row)
    
    print("Customer Query: Tell me when the best so far has stopped improving, so I can stop paying for runs.")
    if found_idx != -1:
        print(f"Analysis: Stopped at row {found_idx + 1}. A configuration in the top 1% of performance was found.")
        print(f"Row data: {rows[found_idx]}")
    else:
        print("Analysis: Processed all rows without finding a configuration that significantly improves upon the baseline.")
    
    exit(0)
