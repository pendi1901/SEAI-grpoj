import ezr
import step01
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining the justification.
    """
    # 1. Estimate the goals for the target row
    # We use the tree-based ranker from step02 to predict the goal values
    # We need to provide a training set to build the model
    tbl = ezr.Tbl([header] + rows)
    node = ezr.tree(tbl, tbl.rows)
    
    # Predict the goal values for the target row
    # Since the row has '?', we use the leaf mean as the estimate
    leaf_node = ezr.leaf(node, row)
    
    # Create a copy of the row to fill in the estimated goals
    estimated_row = list(row)
    for i, name in enumerate(header):
        if name.endswith("-") or name.endswith("+"):
            # Use the mean of the goal column in the leaf
            vals = [r[i] for r in leaf_node.rows if r[i] != "?"]
            estimated_row[i] = sum(vals) / len(vals) if vals else 0
            
    # 2. Calculate how many rows this setup is better than
    # A row is better if its ydist is lower
    target_ydist = ezr.ydist(tbl, estimated_row)
    
    better_count = 0
    for r in rows:
        if ezr.ydist(tbl, r) > target_ydist:
            better_count += 1
            
    p = better_count / len(rows)
    reason = (f"This setup is in the top {int((1-p)*100)}% of all possible configurations "
              f"because its predicted performance metrics outperform {int(p*100)}% of the "
              "historical data based on our decision tree analysis.")
    
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and hide its goals
    target_row = list(rows[0])
    for i, name in enumerate(header):
        if name.endswith("-") or name.endswith("+"):
            target_row[i] = "?"
            
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification Analysis:")
    print(f"Performance percentile: {p:.4f}")
    print(f"Reason: {reason}")
    
    exit(0)
