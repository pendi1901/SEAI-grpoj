import ezr
import random

def justify(header, rows, row):
    """
    Compares a target row against the dataset.
    Returns (p, reason) where p is the fraction of rows that the target row
    is better than, and reason is a human-readable explanation.
    """
    # Build a table to handle normalization and ydist calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Estimate the performance of the target row.
    # Since the target row has '?' for goals, we use the tree-based ranker
    # to predict its performance based on its input columns.
    ranker = ezr.ranker(tbl)
    estimated_ydist = ranker(row)
    
    # Calculate p: fraction of rows that this row is better than.
    # A row is better when its ydist is lower.
    better_than_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = better_than_count / len(rows)
    
    reason = (f"This configuration is better than {p:.1%} of all known setups "
              f"based on its predicted performance across all goals.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Example: Compare two rows (e.g., index 10 vs index 20)
    # The customer asks "I liked B (index 20), you recommended A (index 10). Why not B?"
    idx_a = 10
    idx_b = 20
    
    row_a = list(rows[idx_a])
    row_b = list(rows[idx_b])
    
    # Mask goals for the justification function
    def mask(r):
        new_r = list(r)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_r[i] = "?"
        return new_r

    p_a, reason_a = justify(header, rows, mask(row_a))
    p_b, reason_b = justify(header, rows, mask(row_b))
    
    print(f"Comparison: Recommended Setup (A) vs Customer Choice (B)")
    print(f"Setup A (index {idx_a}): {reason_a}")
    print(f"Setup B (index {idx_b}): {reason_b}")
    
    if p_a >= p_b:
        print(f"\nConclusion: Setup A is superior because it ranks in the top {p_a:.1%} "
              "of configurations, whereas Setup B performs worse.")
    else:
        print(f"\nConclusion: Setup B is actually better than Setup A. "
              "We recommend reconsidering your preference.")
