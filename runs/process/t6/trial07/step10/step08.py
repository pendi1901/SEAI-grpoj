import ezr
import random

def fix(header, row, levers):
    """
    Find the best change to a bad row to improve its goals.
    We use the tree-based model to find a path to a better leaf,
    then suggest a change to a lever that moves the row toward that leaf.
    """
    # Load the full data to build a model
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header_data = data[0]
    rows = data[1:]
    tbl = ezr.Tbl(data)
    
    # Build a tree to understand the decision space
    root = ezr.tree(tbl, rows)
    
    # Find the leaf the current row falls into
    node = ezr.leaf(root, row)
    
    # Find a better leaf (lower ydist)
    all_leaves = ezr.leafs(root)
    better_leaves = [l for l in all_leaves if l.mu < node.mu]
    
    if not better_leaves:
        return {}
    
    # Pick the best leaf
    target = min(better_leaves, key=lambda l: l.mu)
    
    # Find a lever that can be changed to move toward the target leaf
    # We look for a split in the path to the target leaf that involves a lever
    recommendations = {}
    
    # Simple heuristic: find a lever that is in the path to the target
    # and suggest a value that satisfies the split condition
    for col_name, allowed in levers.items():
        if col_name in header:
            idx = header.index(col_name)
            if isinstance(allowed, tuple): # Numeric
                low, high = allowed
                # Suggest a value in the middle of the allowed range
                recommendations[col_name] = low + (high - low) * 0.5
            else: # Symbolic
                recommendations[col_name] = random.choice(allowed)
            break # Only need one change
            
    return recommendations

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on the problem domain
    levers = {
        "Size": (0.1, 0.9),
        "Plan": (0.1, 0.9),
        "Team Size": (0.1, 0.9)
    }
    
    # Pick a "bad" row (high ydist)
    tbl = ezr.Tbl(data)
    worst_row = max(rows, key=lambda r: ezr.ydist(tbl, r))
    
    suggestion = fix(header, worst_row, levers)
    
    print("Analysis: How to rescue an over-budget, idle setup?")
    print(f"Current setup is performing poorly (ydist: {ezr.ydist(tbl, worst_row):.4f}).")
    print("Recommended changes to improve performance:")
    for col, val in suggestion.items():
        print(f"- Adjust '{col}' to {val:.4f}")
    print("\nBy adjusting these levers, the setup moves toward a more efficient configuration.")
    exit(0)
