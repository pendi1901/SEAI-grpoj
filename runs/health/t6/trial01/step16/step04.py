import ezr
import step01

def flow(header, row, seen):
    """
    Decide whether to stop at the current row based on whether it is 
    'good enough'. We define 'good enough' as being in the top 5% 
    of the expected distribution of the entire dataset.
    """
    # If this is the first row, we have no context to judge it.
    if not seen:
        return False
    
    # Create a table to calculate ydist (distance to ideal goals)
    # We use the current row and all seen rows to establish the context
    data = [header] + seen + [row]
    tbl = ezr.Tbl(data)
    
    # Calculate the ydist of the current row
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows to establish a threshold
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # We define "good enough" as being better than the 95th percentile 
    # of the rows seen so far (i.e., in the top 5%).
    # We require at least 20 rows to have been seen to make this judgment.
    if len(seen) >= 20:
        threshold = sorted(seen_ydists)[len(seen_ydists) // 20]
        if current_ydist <= threshold:
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
            print(f"Stopped at row {i} (0-indexed).")
            print(f"Row details: {row}")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("No row met the criteria for early stopping.")
