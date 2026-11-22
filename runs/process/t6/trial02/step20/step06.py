import ezr
import step01
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the performance.
    """
    # Create a table to calculate ydist
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the input row using the tree-based ranker
    # We use the training data (all rows) to build the model
    ranker = step02.guess(header, rows, [row])
    
    # Since step02.guess returns a list of estimates for each goal column,
    # we need to reconstruct the row with estimated values to calculate ydist.
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Create a copy and fill in the estimated goals
    estimated_row = list(row)
    # The ranker in step02 returns the mean of the first goal column.
    # For a full justification, we need to estimate all goals.
    # We'll use the leaf mean for each goal column.
    node = ezr.tree(tbl, tbl.rows)
    leaf = ezr.leaf(node, row)
    
    for i in goal_indices:
        vals = [r[i] for r in leaf.rows if r[i] != "?"]
        estimated_row[i] = sum(vals) / len(vals) if vals else tbl.cols[i].mu
        
    # Calculate ydist for the estimated row
    est_ydist = ezr.ydist(tbl, estimated_row)
    
    # Compare against all rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    better_count = sum(1 for d in all_ydists if d > est_ydist)
    p = better_count / len(rows)
    
    reason = (f"This setup is in the top {int((1-p)*100)}% of all possible configurations "
              f"because its predicted performance metrics are closer to the ideal "
              f"than {int(p*100)}% of the known data.")
    
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Pick a sample row and mask its goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification for selected setup:")
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
    
    exit(0)
