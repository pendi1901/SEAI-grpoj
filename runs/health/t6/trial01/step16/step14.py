import ezr
import step04

def flow(header, row, seen):
    """
    Decide whether to stop at the current row. We stop if the current row
    is significantly better than the best row seen so far, using the 
    statistical comparison logic from ezr to ensure the improvement 
    is not just noise.
    """
    if len(seen) < 20:
        return False
    
    # Create a table to calculate ydist
    tbl = ezr.Tbl([header] + seen + [row])
    
    # Calculate ydist for all seen rows and the current row
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    current_ydist = ezr.ydist(tbl, row)
    
    # We stop if the current row is better than the best 5% of what we've seen
    # AND it represents a statistically significant improvement over the 
    # current best.
    best_seen = min(seen_ydists)
    
    # If the current row is better than the best seen so far
    if current_ydist < best_seen:
        # Check if this improvement is statistically significant
        # We use the same logic as step03/step13 to verify the improvement
        # is not just noise.
        if not ezr.same(sorted(seen_ydists), sorted(seen_ydists + [current_ydist])):
            return True
            
    return False

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Optimization stopped at row {i}.")
            print(f"Row {i} is a statistically significant improvement.")
            print(f"Row details: {row}")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("No row met the criteria for early stopping; processed all data.")
