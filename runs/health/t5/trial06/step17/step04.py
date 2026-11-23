import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    distribution of ydist values, based on the history seen so far.
    """
    if not seen:
        return False
    
    # Create a temporary table to calculate ydist
    # We use the history to establish the context of what is 'good'
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for all seen rows
    ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Calculate the threshold (e.g., the 5th percentile of seen performance)
    # If the current row is better than 95% of what we've seen, stop.
    ydists.sort()
    threshold = ydists[int(len(ydists) * 0.05)]
    
    # Current row's ydist
    current_ydist = ezr.ydist(tbl, row)
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    found_index = -1
    
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_index = i
            break
        seen.append(row)
        
    if found_index != -1:
        print(f"Stopped at row {found_index} (out of {len(rows)}).")
        print(f"The selected setup is: {rows[found_index]}")
    else:
        print("No setup met the criteria before the end of the data.")
        
    exit(0)
