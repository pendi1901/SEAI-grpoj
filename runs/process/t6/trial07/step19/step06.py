import ezr
import step01
import step02

def justify(header, rows, row):
    """
    Returns a pair (p, reason): p is the fraction of rows that 'row' is better than;
    reason is a sentence explaining the ranking.
    """
    # Create a table to handle normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the input row using the tree-based approach from step02
    # We need to fill in the '?' goals to calculate ydist
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Build a tree to estimate the goal values
    # We use the tree to predict the ydist directly
    def get_ydist_mean(node):
        return sum(ezr.ydist(tbl, r) for r in node.rows) / len(node.rows)

    def build_tree(tbl, rows):
        node = ezr.o(rows=rows, at=None, v=None, go=None, kids=[], 
                     mu=sum(ezr.ydist(tbl, r) for r in rows)/len(rows))
        if len(rows) > ezr.the.Leaf and (found := ezr.cut(tbl, rows)):
            at, v, go = found
            yes, no = [], []
            for r in rows: (yes if go(r) else no).append(r)
            node.at, node.v, node.go = at, v, go
            node.kids = [build_tree(tbl, yes), build_tree(tbl, no)]
        return node

    tree_root = build_tree(tbl, rows)
    
    # Estimate the ydist for the target row
    estimated_ydist = ezr.leaf(tree_root, row).mu
    
    # Calculate how many rows are worse than this estimated ydist
    # A row is better if its ydist is lower.
    # We are better than a row if our ydist is lower than theirs.
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    better_than_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = better_than_count / len(rows)
    
    reason = f"This setup is estimated to be in the top {int((1-p)*100)}% of all possible configurations based on its input characteristics."
    
    return p, reason

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals
    target_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for idx in goal_indices:
        target_row[idx] = "?"
        
    p, reason = justify(header, rows, target_row)
    
    print(f"Ranking: {p:.4f}")
    print(f"Justification: {reason}")
    exit(0)
