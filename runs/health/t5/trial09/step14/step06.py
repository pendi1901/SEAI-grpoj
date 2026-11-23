import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining why.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # To compare 'row' against 'rows', we need to estimate the goals of 'row'.
    # We use a simple tree-based ranker to estimate the ydist of 'row'.
    # We build the tree on all available data.
    node = ezr.tree(tbl, rows)
    
    # The ranker returns the mean ydist of the leaf where the row lands.
    # Lower ydist is better.
    ranker = lambda r: ezr.leaf(node, r).mu
    
    # Calculate the estimated ydist for the target row
    target_ydist = ranker(row)
    
    # Calculate ydist for all existing rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that are worse than the target row.
    # A row is better if its ydist is smaller.
    # We count how many rows have a ydist greater than our target.
    better_than_count = sum(1 for y in all_ydists if y > target_ydist)
    p = better_than_count / len(rows)
    
    # Construct a human-readable reason
    reason = (f"This setup is better than {int(p * 100)}% of all known configurations "
              "because its input parameters lead to a predicted performance "
              "closer to the ideal goal values.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Pick a random row to justify, masking its goals
    target_row = list(random.choice(rows))
    for i, name in enumerate(header):
        if name[-1] in "+-":
            target_row[i] = "?"
            
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification: {reason}")
    print(f"Performance percentile: {p:.2f}")
    
    exit(0)
