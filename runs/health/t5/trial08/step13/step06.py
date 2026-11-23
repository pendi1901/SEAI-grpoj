import ezr

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a human-readable explanation of why this setup is good.
    """
    # Create a table to handle normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the target row
    # We use a simple tree-based ranker to estimate the ydist of the target row
    # based on its input columns (x)
    ranker = ezr.ranker(tbl)
    estimated_ydist = ranker(row)
    
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that 'row' is better than
    # 'row' is better than another row if its ydist is smaller
    better_than_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = better_than_count / len(rows)
    
    # Construct a reason
    # We identify the most influential input column (the one with the highest variance)
    # or simply state the performance percentile.
    reason = (f"This setup is in the top {int((1-p)*100)}% of all configurations "
              f"evaluated, as it minimizes the distance to optimal goals better "
              f"than {int(p*100)}% of the known alternatives.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Pick a sample row to justify (e.g., the 10th row)
    # Mask its goals to simulate the "unknown" scenario
    target_row = list(rows[10])
    masked_row = ["?" if i < 3 else val for i, val in enumerate(target_row)]
    
    p, reason = justify(header, rows, masked_row)
    
    print("Customer Query: You say this setup is good. How good, against all the others, and why should I believe it?")
    print(f"Result: {reason}")
    print(f"Confidence score (p): {p:.4f}")
    
    exit(0)
