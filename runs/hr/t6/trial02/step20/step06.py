import ezr
import step01
import step02
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that `row` is better than.
    `row` is estimated using a tree built on the provided `rows`.
    """
    # Build a model on all rows to estimate the goals for the target row
    tbl = ezr.Tbl([header] + rows)
    
    # Use the tree-based ranker to estimate the ydist of the target row
    # We need to estimate the goal values for the target row first.
    # Since the target row has '?' in goal columns, we use the leaf mean.
    root = ezr.tree(tbl, tbl.rows)
    
    # Estimate ydist for the target row
    # The ranker logic: leaf mean of ydist
    target_node = ezr.leaf(root, row)
    target_ydist = target_node.mu
    
    # Calculate how many rows are worse (higher ydist) than the target
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    worse_count = sum(1 for y in all_ydists if y > target_ydist)
    p = worse_count / len(rows)
    
    # Construct a reason based on the tree path
    path = []
    curr = root
    while curr.kids:
        op = "=" if type(tbl.cols[curr.at]) is ezr.Sym else "<="
        val = curr.v
        path.append(f"{header[curr.at]} {op} {val}")
        curr = curr.kids[0] if curr.go(row) else curr.kids[1]
        
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% because it follows the pattern: " + " and ".join(path) + "."
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a random row to justify
    test_row = list(random.choice(rows))
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification Analysis:")
    print(f"Rank: {p:.2f} (fraction of population outperformed)")
    print(f"Reason: {reason}")
    
    exit(0)
