import ezr
import step01
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that `row` is better than,
    and a reason string explaining the performance.
    """
    # Build a table to define column roles and calculate metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the performance (ydist) for the input row.
    # The ranker returns the mean ydist of the leaf node the row falls into.
    ranker = ezr.ranker(tbl)
    est_ydist = ranker(row)
    
    # Calculate ydist for all existing rows to compare.
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that have a worse (higher) ydist than our estimate.
    # A row is better if its ydist is lower.
    # So, row is better than r if est_ydist < ydist(r).
    better_than = [d for d in all_ydists if est_ydist < d]
    p = len(better_than) / len(rows)
    
    reason = (f"This setup is estimated to be better than {p:.0%} of all "
              "available configurations based on its input parameters.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Pick a sample row and mask its goals to test the justification
    test_row = list(all_rows[0])
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, all_rows, test_row)
    
    print(f"Justification: {reason}")
    print(f"Confidence score (p): {p:.4f}")
    
    exit(0)
