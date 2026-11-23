import ezr
import random

def flow(header, row, seen):
    """
    Warn the customer the moment a process starts to go bad.
    We define 'going bad' as a significant increase in ydist (performance degradation)
    compared to the historical performance of the process.
    
    We use a sliding window of the last 20 rows to establish a baseline of 
    'normal' performance. If the current row's ydist is significantly worse 
    (e.g., > 2 standard deviations above the mean) than the recent baseline, 
    we flag it as 'bad'.
    """
    if len(seen) < 20:
        return False
    
    # Create a table context from the seen rows to calculate ydist
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for the current row and the recent history
    current_ydist = ezr.ydist(tbl, row)
    recent_rows = seen[-20:]
    recent_ydists = [ezr.ydist(tbl, r) for r in recent_rows]
    
    # Calculate mean and standard deviation of recent performance
    mu = sum(recent_ydists) / len(recent_ydists)
    sd = (sum((x - mu)**2 for x in recent_ydists) / len(recent_ydists))**0.5
    
    # If the current row is significantly worse than the recent average,
    # we return True to signal that the process is starting to go bad.
    # We use a threshold of 2 standard deviations.
    if current_ydist > (mu + 2 * sd):
        return True
        
    return False

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    # Simulate the arrival process
    # We do not shuffle here to preserve the temporal order of the data
    seen = []
    found_bad = False
    
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Warning: Process degradation detected at row index {i}!")
            print(f"The current configuration is performing significantly worse than recent history.")
            found_bad = True
            break
        seen.append(row)
        
    if not found_bad:
        print("Process monitoring complete: No significant degradation detected.")
        
    exit(0)
