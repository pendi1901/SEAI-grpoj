import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    To simulate requirements changing twice as fast halfway through,
    we weight the training data: rows from the second half of the 
    training set are given more influence (higher weight) in the 
    tree-based estimation model.
    """
    # Identify the index of the first goal column
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    first_goal_idx = goal_indices[0]
    
    # Create a table for the training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a custom tree where each node stores the weighted mean of the first goal.
    # We weight rows from the second half (index >= len(train)/2) twice as much.
    def get_weighted_mean(rows):
        total_val = 0
        total_weight = 0
        mid = len(train) // 2
        for r in rows:
            # Find original index to determine if it's in the second half
            # Since we don't have indices, we use the row's position in the original train list
            # We can map rows back to their original index by reference or by searching
            weight = 2 if train.index(r) >= mid else 1
            total_val += r[first_goal_idx] * weight
            total_weight += weight
        return total_val / total_weight if total_weight > 0 else 0

    def build_tree(tbl, rows):
        node = ezr.o(rows=rows, at=None, v=None, go=None, kids=[], 
                     mu=get_weighted_mean(rows))
        if len(rows) > ezr.the.Leaf and (found := ezr.cut(tbl, rows)):
            at, v, go = found
            yes, no = [], []
            for r in rows: (yes if go(r) else no).append(r)
            node.at, node.v, node.go = at, v, go
            node.kids = [build_tree(tbl, yes), build_tree(tbl, no)]
        return node

    tree_root = build_tree(train_tbl, train)
    
    # For each test row, walk the tree to the leaf and return the leaf's weighted mean
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
    
    # Mask the goals in the test set
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    print("Analysis: Impact of accelerating requirements change.")
    print(f"Estimated average for first goal (Cost-) under accelerated change: {sum(estimates)/len(estimates):.4f}")
    print("By weighting the second half of the training data, we account for the increased volatility.")
    exit(0)
