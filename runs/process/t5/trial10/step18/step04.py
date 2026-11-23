import ezr
import random

def flow(header, row, seen):
    """
    Decide whether to accept a row based on whether it is better than 
    the current best seen so far.
    """
    # If this is the first row, we have no baseline, so we accept it.
    if not seen:
        return True
    
    # Create a table to handle normalization and goal distance calculations
    # We use the header and the history of seen rows to define the context
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the quality of the current row and the best row seen so far
    # ydist returns 0 for ideal, higher for worse.
    current_ydist = ezr.ydist(tbl, row)
    best_ydist = min(ezr.ydist(tbl, r) for r in seen)
    
    # If the current row is better (lower ydist) than the best seen, accept it.
    # We use a small threshold to avoid accepting rows that are effectively identical.
    return current_ydist < (best_ydist * 0.95)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    accepted = []
    
    for row in rows:
        if flow(header, row, seen):
            accepted.append(row)
        seen.append(row)
    
    print(f"Processed {len(rows)} proposals.")
    print(f"Accepted {len(accepted)} proposals based on the 'better than previous best' criteria.")
    
    # Summary of the quality of accepted rows
    if accepted:
        tbl = ezr.Tbl([header] + rows)
        avg_ydist = sum(ezr.ydist(tbl, r) for r in accepted) / len(accepted)
        print(f"Average quality (ydist) of accepted proposals: {avg_ydist:.4f}")
