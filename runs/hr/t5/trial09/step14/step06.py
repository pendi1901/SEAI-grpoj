import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a reason explaining the ranking based on the tree-based model.
    """
    # Build a model on all known rows
    tbl = ezr.Tbl([header] + rows)
    node = ezr.tree(tbl, rows)
    
    # Estimate ydist for the target row by finding its leaf
    # Since goal cells are '?', we use the leaf's mean ydist
    target_leaf = ezr.leaf(node, row)
    target_ydist = target_leaf.mu
    
    # Calculate how many rows are worse than this target
    # A row is worse if its ydist is higher (further from goals)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    worse_count = sum(1 for d in all_ydists if d > target_ydist)
    p = worse_count / len(rows)
    
    # Construct a reason based on the tree path
    reason = (f"This arrangement ranks in the top {int((1-p)*100)}% of all records "
              f"because it falls into a leaf node with an average ydist of {target_ydist:.2f}, "
              f"outperforming {int(p*100)}% of the historical data.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a random row to justify, mask its goals
    target_row = random.choice(rows)
    masked_row = list(target_row)
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    for idx in goal_indices:
        masked_row[idx] = "?"
        
    p, reason = justify(header, rows, masked_row)
    
    print(f"Justification for the selected arrangement:")
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
