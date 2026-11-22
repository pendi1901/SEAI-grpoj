import ezr
import random

def justify(header, rows, row):
    """
    Compares a proposed 'row' against all 'rows' by estimating its performance.
    Returns (p, reason) where p is the fraction of rows that 'row' is better than.
    """
    # Create a table to handle normalization and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # To estimate the performance of the provided row (which has '?' in goals),
    # we use the tree-based ranker to predict its ydist.
    ranker = ezr.ranker(tbl)
    estimated_ydist = ranker(row)
    
    # Calculate ydist for all known rows to compare against
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # A row is better if its ydist is lower.
    # Count how many rows are worse (have a higher ydist) than our estimate.
    better_than_count = sum(1 for y in all_ydists if y > estimated_ydist)
    p = better_than_count / len(rows)
    
    # Construct the reason string
    reason = (f"This setup is estimated to be better than {int(p*100)}% "
              f"of all known configurations based on its input characteristics.")
    
    return p, reason

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Select two rows to compare: 
    # Setup A (the recommended one, e.g., index 0)
    # Setup B (the one the customer liked, e.g., index 1)
    idx_a, idx_b = 0, 1
    row_a = list(rows[idx_a])
    row_b = list(rows[idx_b])
    
    # Mask the goal columns for the justification function
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        row_a[idx] = "?"
        row_b[idx] = "?"
        
    p_a, reason_a = justify(header, rows, row_a)
    p_b, reason_b = justify(header, rows, row_b)
    
    print(f"--- Comparison: Setup A vs Setup B ---")
    print(f"Setup A percentile: {p_a:.4f}")
    print(f"Setup B percentile: {p_b:.4f}")
    print(f"\nJustification for A: {reason_a}")
    print(f"Justification for B: {reason_b}")
    
    if p_a >= p_b:
        print("\nConclusion: Setup A is recommended because it is estimated to perform "
              "better than a larger fraction of the known configuration space than Setup B.")
    else:
        print("\nConclusion: Setup B is actually estimated to be stronger; "
              "the recommendation for A may need re-evaluation.")
