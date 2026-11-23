import ezr
import step01

def flow(header, row, seen):
    """
    Decide whether to stop at the current row.
    We define 'good enough' as being in the top 5% of the potential 
    distribution of the dataset, estimated by the ydist metric.
    """
    # If this is the first row, we can't compare yet
    if not seen:
        return False
    
    # Create a table to use the ydist metric
    # We use the current row and all seen rows to establish the context
    data = [header] + seen + [row]
    tbl = ezr.Tbl(data)
    
    # Calculate the ydist for the current row
    # Lower ydist is better (closer to ideal goals)
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Define 'good enough' as being better than 95% of what we've seen
    # or better than the best seen so far if we have enough history.
    # Here, we stop if the current row is in the top 5% of the seen distribution.
    if len(seen) > 20:
        threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
        if current_ydist <= threshold:
            return True
            
    return False

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
        
        seen = []
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stopped at row {i}: {row}")
                found = True
                break
            seen.append(row)
            
        if not found:
            print("No configuration met the 'good enough' criteria.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    exit(0)
