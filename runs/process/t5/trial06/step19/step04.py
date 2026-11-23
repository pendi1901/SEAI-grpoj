import ezr
import random

def flow(header, row, seen):
    """
    Decide whether to approve a row immediately.
    We compare the current row's potential against the best seen so far.
    If the current row is significantly better than the average of the 
    best 10% seen so far, we approve it.
    """
    if not seen:
        return True
    
    # Create a table to handle normalization and goal distance
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all seen rows
    # Lower ydist is better
    seen_scores = [ezr.ydist(tbl, r) for r in seen]
    
    # Identify the threshold: the average of the best 10% seen so far
    seen_scores.sort()
    limit = max(1, len(seen_scores) // 10)
    threshold = sum(seen_scores[:limit]) / limit
    
    # Calculate ydist for the current row
    # We use the existing table's column logic to normalize the new row
    current_score = ezr.ydist(tbl, row)
    
    # Approve if the current row is better (lower distance) than the threshold
    return current_score <= threshold

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival
    random.seed(1234567891)
    random.shuffle(rows)
    
    approved = []
    seen = []
    
    for row in rows:
        if flow(header, row, seen):
            approved.append(row)
        seen.append(row)
    
    # Summary for the customer
    print(f"Decision process complete.")
    print(f"Total proposals reviewed: {len(rows)}")
    print(f"Proposals approved: {len(approved)}")
    
    # Calculate average quality of approved vs total
    tbl = ezr.Tbl([header] + rows)
    avg_all = sum(ezr.ydist(tbl, r) for r in rows) / len(rows)
    avg_app = sum(ezr.ydist(tbl, r) for r in approved) / len(approved)
    
    print(f"Average ydist of all proposals: {avg_all:.4f}")
    print(f"Average ydist of approved proposals: {avg_app:.4f}")
    print("Lower ydist indicates better performance.")
    
    exit(0)
