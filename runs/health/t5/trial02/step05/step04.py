import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    performance distribution based on the data seen so far.
    """
    # Create a table to handle column roles and ydist calculations
    # We use the header to define the structure
    tbl = ezr.Tbl([header] + (seen if seen else [row]))
    
    # Calculate the ydist of the current row
    current_ydist = ezr.ydist(tbl, row)
    
    # If this is the first row, we can't compare it yet
    if not seen:
        return False
    
    # Calculate ydist for all previously seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # We define 'good enough' as being better than 95% of what we've seen
    # or better than a reasonable threshold if we have enough data.
    # Here, we check if the current row is in the top 5% of the seen distribution.
    threshold = sorted(seen_ydists)[max(0, int(len(seen_ydists) * 0.05))]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopped at row {i+1}. Found a high-quality setup.")
            print("Setup details:")
            for h, v in zip(header, row):
                print(f"  {h}: {v}")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("Reached the end of the data without finding a 'good enough' setup.")
