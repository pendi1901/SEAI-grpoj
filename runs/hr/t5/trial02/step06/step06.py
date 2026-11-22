import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than;
    reason is a sentence explaining the ranking.
    """
    # Create a table to handle the data and calculate ydist
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all known rows
    # ydist is the distance from the ideal goal values (lower is better)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # To estimate the goal values for the input 'row', we use the tree
    # to find the leaf node that matches the input characteristics.
    # The leaf's mean ydist serves as our estimate for the row's performance.
    root = ezr.tree(tbl, rows)
    leaf_node = ezr.leaf(root, row)
    estimated_ydist = leaf_node.mu
    
    # Calculate p: fraction of rows that are worse than our estimated row
    # (i.e., have a higher ydist)
    worse_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = worse_count / len(rows)
    
    # Generate a reason based on the ranking
    reason = (f"This arrangement ranks in the top {int((1-p)*100)}% of all observed "
              f"employee records based on our multi-objective performance model.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a random row to test, mask its goals
    test_row = list(random.choice(rows))
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Ranking: {p:.2f}")
    print(f"Justification: {reason}")
    
    exit(0)
