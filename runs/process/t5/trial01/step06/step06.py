import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that the given row is better than,
    and reason is a sentence explaining the performance.
    """
    # Create a table to handle column logic and normalization
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows (lower is better)
    # We use the full rows to establish the ground truth
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Estimate the ydist for the target row.
    # Since goal cells are "?", we use the tree-based ranker to estimate 
    # the expected ydist based on the input columns.
    ranker_func = ezr.ranker(tbl)
    target_ydist = ranker_func(row)
    
    # Calculate p: fraction of rows that are worse than the target row
    # (i.e., have a higher ydist)
    better_than_count = sum(1 for d in all_ydists if d > target_ydist)
    p = better_than_count / len(rows)
    
    # Construct the reason
    reason = (f"This configuration is in the top {int((1-p)*100)}% of all "
              f"possible setups based on our performance model.")
    
    return p, reason

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    # Pick a random row to justify
    random.seed(1234567891)
    target_row = random.choice(rows)
    
    # Mask the goals in the target row as per instructions
    masked_row = list(target_row)
    for i, name in enumerate(header):
        if name[-1] in "+-":
            masked_row[i] = "?"
            
    # Get justification
    p, reason = justify(header, rows, masked_row)
    
    print("Justification Report:")
    print(f"Target Row: {masked_row}")
    print(f"Rank (p): {p:.4f}")
    print(f"Reason: {reason}")
    
    exit(0)
