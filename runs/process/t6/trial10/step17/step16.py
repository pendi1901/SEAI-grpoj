import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Explains why a specific row (B) might be less desirable than the 
    recommended configuration (A) by comparing their predicted performance.
    """
    # Create a table to calculate ydist for all rows
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the target row using the tree-based ranker
    # We use the training data (all rows) to build the model
    node = ezr.tree(tbl, tbl.rows)
    leaf_node = ezr.leaf(node, row)
    
    # Estimate all goal columns based on the leaf's average
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith("-") or name.endswith("+")]
    
    estimated_row = row[:]
    for idx in goal_indices:
        vals = [r[idx] for r in leaf_node.rows if r[idx] != "?"]
        estimated_row[idx] = sum(vals) / len(vals) if vals else 0
        
    # Calculate how many rows are worse than this estimated row
    target_ydist = ezr.ydist(tbl, estimated_row)
    worse_count = sum(1 for r in rows if ezr.ydist(tbl, r) > target_ydist)
    
    p = worse_count / len(rows)
    
    # Compare with the best possible performance (the global minimum ydist)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    best_ydist = min(all_ydists)
    
    # Construct the explanation
    reason = (f"While your chosen setup is better than {int(p * 100)}% of configurations, "
              f"it remains {target_ydist - best_ydist:.2f} units away from the "
              "optimal performance achievable in this environment.")
    
    return p, reason

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    try:
        header = next(rows_gen)
        rows = list(rows_gen)
        
        # Pick a sample row to represent 'Setup B' and mask its goals
        test_row = rows[10][:]
        test_row[-3:] = ["?", "?", "?"]
        
        p, reason = justify(header, rows, test_row)
        print(f"Ranking: {p:.4f}")
        print(f"Justification: {reason}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    exit(0)
