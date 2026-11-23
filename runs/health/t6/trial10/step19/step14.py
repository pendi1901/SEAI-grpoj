import ezr
import step01

def flow(header, row, seen):
    """
    Decide if the current row is the best seen so far.
    We stop when the current row is significantly better than all 
    previous rows, or if we have seen enough to be confident.
    """
    if not seen:
        return False
    
    # Create a table from the history to establish the distribution
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the ydist of the current row
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If the current row is better (lower ydist) than all previous rows,
    # we consider it a significant improvement.
    # We also require a minimum number of samples to avoid stopping too early.
    if len(seen) > 20 and current_ydist < min(seen_ydists):
        return True
        
    return False

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    header = all_rows[0]
    rows = all_rows[1:]
    
    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopping criteria met at row {i}.")
            print(f"Best configuration found: {row}")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("No configuration met the stopping criteria; processed all rows.")
