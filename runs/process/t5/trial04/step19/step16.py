import ezr
import random

def justify(header, rows, row):
    """
    Compares a target row against all known rows.
    Returns (p, reason): p is the fraction of rows that 'row' is better than.
    'row' has '?' in goal columns; we estimate its performance using a tree.
    """
    # Build a model on all known rows to estimate the performance of the target row
    tbl = ezr.Tbl([header] + rows)
    node = ezr.tree(tbl, rows)
    
    # Estimate the ydist of the input row by finding its leaf
    # ydist is the distance to the ideal, so lower is better.
    leaf_node = ezr.leaf(node, row)
    estimated_ydist = leaf_node.mu
    
    # Calculate how many rows are worse than this estimate
    # A row is worse if its ydist is higher than our estimated ydist
    worse_count = 0
    for r in rows:
        if ezr.ydist(tbl, r) > estimated_ydist:
            worse_count += 1
            
    p = worse_count / len(rows)
    
    reason = (f"Your chosen setup is estimated to be better than {p:.2%} "
              "of all historical configurations based on its input parameters.")
    
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Pick two random rows to simulate the customer's choice (B) and our recommendation (A)
    # We mask the goals for the justification function
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Let's assume row 10 is the customer's choice (B)
    target_row = list(rows[10])
    for idx in goal_indices:
        target_row[idx] = "?"
        
    p, reason = justify(header, rows, target_row)
    
    print("Justification Report: Why not setup B?")
    print("-" * 60)
    print(reason)
    print(f"Confidence score (p): {p:.4f}")
    print("-" * 60)
    print("Note: A higher p-value indicates that the setup is superior to a larger")
    print("portion of the historical data.")
    
    exit(0)
