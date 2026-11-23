import ezr
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining the justification.
    """
    # Create a table to handle normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the target row using the tree-based approach from step02
    # We need to fill the '?' in the target row to calculate its ydist
    # We use the training data (rows) to build the model
    model = ezr.tree(tbl, rows)
    
    # Create a copy of the row to fill in the goals
    row_with_goals = list(row)
    leaf = ezr.leaf(model, row)
    for col in tbl.y:
        # Calculate mean of this goal in the leaf
        vals = [r[col.at] for r in leaf.rows]
        row_with_goals[col.at] = sum(vals) / len(vals)
    
    # Calculate ydist for the target row and all other rows
    target_ydist = ezr.ydist(tbl, row_with_goals)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that have a higher (worse) ydist than our target
    # (i.e., how many rows are worse than this one)
    better_than_count = sum(1 for d in all_ydists if d > target_ydist)
    p = better_than_count / len(rows)
    
    reason = (f"This setup is in the top {int((1-p)*100)}% of all configurations "
              "based on its predicted performance metrics.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row to justify, masking its goals
    target_row = list(rows[0])
    for i, name in enumerate(header):
        if name[-1] in "+-":
            target_row[i] = "?"
            
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification: {reason}")
    print(f"Performance percentile: {p:.4f}")
    exit(0)
