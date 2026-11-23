import ezr
import step01

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker from ezr to find the leaf mean of the first goal.
    """
    # Create a table for the training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Identify the index of the first goal column
    # Goals are columns ending in '-' or '+'
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    first_goal_idx = goal_indices[0]
    
    # Build a tree on the training data
    # We need to predict the value of the first goal column
    # We can adapt the tree structure to store the mean of the first goal
    # instead of the mean of ydist.
    
    def get_goal_mean(node):
        vals = [r[first_goal_idx] for r in node.rows]
        return sum(vals) / len(vals)

    # Build a custom tree where each node stores the mean of the first goal
    def build_tree(tbl, rows):
        node = ezr.o(rows=rows, at=None, v=None, go=None, kids=[], 
                     mu=sum(r[first_goal_idx] for r in rows)/len(rows))
        if len(rows) > ezr.the.Leaf and (found := ezr.cut(tbl, rows)):
            at, v, go = found
            yes, no = [], []
            for r in rows: (yes if go(r) else no).append(r)
            node.at, node.v, node.go = at, v, go
            node.kids = [build_tree(tbl, yes), build_tree(tbl, no)]
        return node

    tree_root = build_tree(train_tbl, train)
    
    # For each test row, walk the tree to the leaf and return the leaf's mean
    results = []
    for row in test:
        node = ezr.leaf(tree_root, row)
        results.append(node.mu)
        
    return results

if __name__ == "__main__":
    # Load data
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Split: 800 training, 200 testing
    train = rows[:800]
    test = rows[800:]
    
    # Mask the goals in the test set to simulate "unknown"
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print summary
    print("Estimation Results (First Goal Column):")
    print(f"Estimated average for first goal: {sum(estimates)/len(estimates):.4f}")
    print(f"Sample estimate for first test row: {estimates[0]:.4f}")
    exit(0)
