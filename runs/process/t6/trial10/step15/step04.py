import ezr
import random

def flow(header, row, seen):
    """
    Decide whether to accept a row based on whether it is better than
    the current best seen so far. Since we need to stop eventually,
    we accept if the row is in the top 5% of the expected distribution
    or if we have seen enough rows to be confident.
    """
    if not seen:
        return False
    
    # Create a table to use ydist for scoring
    # We use the seen rows to establish the context of 'good'
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for the current row and all seen rows
    # A lower ydist is better.
    current_ydist = ezr.ydist(tbl, row)
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If this row is better than 95% of what we have seen, accept it.
    # This acts as a threshold for "good enough to stop".
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    try:
        header = next(rows_gen)
        all_rows = list(rows_gen)
    except StopIteration:
        exit(1)

    # Simulate the arrival process
    random.shuffle(all_rows)
    seen = []
    accepted = None
    
    for i, row in enumerate(all_rows):
        if flow(header, row, seen):
            accepted = (i, row)
            break
        seen.append(row)
    
    if accepted:
        print(f"Accepted row at index {accepted[0]} after seeing {len(seen)} rows.")
        print(f"Row data: {accepted[1]}")
    else:
        print("No row met the acceptance criteria.")
    
    exit(0)
