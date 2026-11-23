import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to stop the process. We stop if the current row is 
    significantly better than the best seen so far, or if we have seen 
    enough rows without improvement.
    
    Logic: If the current row is in the top 5% of the history, we consider 
    it a 'best' candidate. We stop if we have seen at least 50 rows and 
    no new 'best' has appeared in the last 20 rows.
    """
    if len(seen) < 50:
        return False

    # Check if the current row is a 'best' performer
    all_rows = seen + [row]
    best_indices = remember(header, all_rows)
    
    # If the current row is in the top 5%, it's an improvement
    if len(all_rows) - 1 in best_indices:
        return False # Keep going, we found a new best
    
    # If we haven't found a new best in the last 20 rows, stop
    recent_rows = seen[-20:]
    for i, r in enumerate(recent_rows):
        # If any of the last 20 were 'best', we are still improving
        if (len(seen) - 20 + i) in best_indices:
            return False
            
    return True

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        seen = []
        stopped = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Improvement has plateaued. Stopping at row {i}.")
                stopped = True
                break
            seen.append(row)
            
        if not stopped:
            print("Processing complete. No plateau detected.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
