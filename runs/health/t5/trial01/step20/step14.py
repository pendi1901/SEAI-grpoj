import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    performance distribution based on the rows seen so far.
    """
    if not seen:
        return False
    
    # Create a table to use ezr's distance metrics
    # We use the seen rows to establish the context of what is 'good'
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the ydist (distance from ideal) for all seen rows
    # Lower ydist is better.
    scores = [ezr.ydist(tbl, r) for r in seen]
    
    # Calculate the current row's ydist
    current_score = ezr.ydist(tbl, row)
    
    # If the current row is better than the 95th percentile of seen rows,
    # we consider it 'good enough' to stop.
    threshold = sorted(scores)[max(0, int(len(scores) * 0.05))]
    
    return current_score <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Optimization stopped at row {i+1}.")
            print(f"Found a setup that meets the top 5% performance threshold.")
            print(f"Row data: {row}")
            found = True
            break
        seen.append(row)
        
    if not found:
        print("No setup met the criteria within the provided data.")
    
    exit(0)
