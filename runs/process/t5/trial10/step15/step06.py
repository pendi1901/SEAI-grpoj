import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the percentile rank of the row
    and reason is a human-readable explanation.
    """
    # Build a table to calculate ydist
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Estimate the goals for the input row using the tree ranker
    # We build a tree on all known rows to predict the performance of the input row
    ranker = ezr.ranker(tbl)
    estimated_ydist = ranker(row)
    
    # Calculate ydist for all known rows to establish a distribution
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that this row is better than
    # A row is better if its ydist is lower.
    # We count how many rows have a higher ydist than our estimate.
    better_than_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = better_than_count / len(rows)
    
    reason = (f"This setup is better than {int(p * 100)}% of all known configurations "
              f"based on its predicted performance across all goals.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row to justify (e.g., the 10th row)
    # Mask its goals to simulate the "unknown" state
    target_row = list(rows[10])
    for i, name in enumerate(header):
        if name[-1] in "+-":
            target_row[i] = "?"
            
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification for row 10:")
    print(f"Percentile: {p:.4f}")
    print(f"Reason: {reason}")
