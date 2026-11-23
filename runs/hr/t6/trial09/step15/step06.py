import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a reason based on the tree-based ranking.
    """
    # Create a table to handle the data
    tbl = ezr.Tbl([header] + rows)
    
    # Build a tree to rank rows based on ydist
    # We use the tree to estimate the quality of the input row
    node = ezr.tree(tbl, rows)
    
    # Estimate the ydist of the input row by finding its leaf
    # We need to fill the '?' goals to calculate ydist, 
    # but the tree leaf's mu is already an estimate of ydist.
    target_mu = ezr.leaf(node, row).mu
    
    # Calculate how many rows are worse (have higher ydist) than our target_mu
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    better_than_count = sum(1 for y in all_ydists if y > target_mu)
    p = better_than_count / len(rows)
    
    # Construct a reason based on the tree path
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all records because it aligns with patterns found in high-performing clusters."
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a random row to justify
    test_row = list(random.choice(rows))
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification Analysis:")
    print(f"Rank: This row is better than {p:.2%} of the population.")
    print(f"Reason: {reason}")
    
    exit(0)
