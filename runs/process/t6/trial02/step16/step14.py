import ezr
import step04

def flow(header, row, seen):
    """
    Warn the customer if a new row is 'bad'.
    We define 'bad' as being significantly worse than the median performance
    of the rows seen so far. If the new row's ydist is higher than the 
    median ydist of the seen data, we flag it (return True).
    """
    if not seen:
        return False
    
    # Create a table from seen rows to understand the distribution
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the median ydist of the history
    current_ydists = [ezr.ydist(tbl, r) for r in seen]
    median_ydist = sorted(current_ydists)[len(current_ydists) // 2]
    
    # Calculate ydist for the new row
    # Note: We use the same tbl to ensure normalization is consistent
    new_ydist = ezr.ydist(tbl, row)
    
    # If the new row is worse than the median (higher ydist), warn the user
    return new_ydist > median_ydist

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    seen = []
    warnings = 0
    
    for row in rows:
        if flow(header, row, seen):
            warnings += 1
        seen.append(row)
        
    print(f"Monitoring complete.")
    print(f"Processed {len(rows)} incoming project configurations.")
    print(f"Total 'bad' performance warnings triggered: {warnings}")
    print("Logic: A warning is triggered if a new configuration's performance")
    print("is worse than the median performance of all previously seen configurations.")
    
    exit(0)
