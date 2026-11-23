import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    distribution of ydist scores based on the history seen so far.
    """
    # We need at least a small sample to establish a baseline
    if len(seen) < 20:
        return False
    
    # Create a temporary table to calculate ydist
    # We need the header to identify goals
    tbl = ezr.Tbl([header] + seen + [row])
    
    # Calculate ydist for all seen rows
    # Lower ydist is better
    scores = [ezr.ydist(tbl, r) for r in seen]
    current_score = ezr.ydist(tbl, row)
    
    # If the current row is better than 95% of what we've seen, stop.
    # We use a threshold: if current_score is lower than the 5th percentile
    # of the history, we accept it.
    sorted_scores = sorted(scores)
    threshold = sorted_scores[int(len(sorted_scores) * 0.05)]
    
    return current_score <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Optimization stopped at row {i+1}.")
            print(f"Accepted configuration: {row}")
            found = True
            break
        seen.append(row)
        
    if not found:
        print("No configuration met the criteria within the provided data.")
