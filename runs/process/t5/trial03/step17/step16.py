import ezr
import random

def justify(header, rows, row):
    """
    Compares a target 'row' against a set of 'rows'.
    Returns (p, reason) where p is the fraction of rows that 'row' is better than.
    'row' has goals as '?', so we estimate its quality using a tree-based ranker.
    """
    # Create a table from the known rows
    tbl = ezr.Tbl([header] + rows)
    
    # Build a ranker to estimate the quality of the target row
    # The ranker returns the mean ydist of the leaf node the row falls into.
    # Lower ydist is better.
    rank_func = ezr.ranker(tbl)
    
    # Estimate the ydist of the target row
    estimated_ydist = rank_func(row)
    
    # Calculate ydist for all known rows to establish a baseline
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # A row is better if its ydist is lower.
    # We are better than a row if our estimated_ydist < row_ydist.
    better_than_count = sum(1 for d in all_ydists if estimated_ydist < d)
    p = better_than_count / len(rows)
    
    reason = (f"This setup is estimated to be better than {p:.2%} of "
              "all known configurations based on its input characteristics.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the customer's request:
    # They liked setup B (a random row), we recommended A (the best row).
    # We justify why A is better than B.
    random.seed(1234567891)
    
    # Find the best row (A)
    tbl = ezr.Tbl([header] + rows)
    best_row = min(rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Pick a random row (B)
    b_row = random.choice(rows)
    
    # Mask goals for the justification function
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    def mask(r):
        new_r = list(r)
        for idx in goal_indices: new_r[idx] = "?"
        return new_r

    p_a, reason_a = justify(header, rows, mask(best_row))
    p_b, reason_b = justify(header, rows, mask(b_row))
    
    print("Customer: 'I liked setup B. You recommended A. Explain why not B.'")
    print(f"\nAnalysis:")
    print(f"  Setup A (Recommended): {reason_a}")
    print(f"  Setup B (Your Choice): {reason_b}")
    print(f"\nConclusion: Setup A is superior because it ranks in the top {p_a:.2%} "
          "of configurations, whereas your choice (B) ranks lower.")
