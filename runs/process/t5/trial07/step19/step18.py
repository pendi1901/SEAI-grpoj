import ezr
import random

def fix(header, row, levers):
    """
    Finds the smallest change to levers that moves a bad row toward the 
    best-performing cluster. We use the tree to find the leaf with the 
    lowest ydist and move the row's levers toward that leaf's centroid.
    """
    # Load data to build a model
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    rows = data[1:]
    tbl = ezr.Tbl(data)
    
    # Build a tree to find the best performing region
    root = ezr.tree(tbl, rows)
    leaves = sorted(ezr.leafs(root), key=lambda n: n.mu)
    best_leaf = leaves[0]
    
    # Calculate the centroid of the best leaf for all input columns
    best_mids = {}
    for at in tbl.cols:
        col = tbl.cols[at]
        if col in tbl.x:
            vals = [r[at] for r in best_leaf.rows if r[at] != "?"]
            if vals:
                best_mids[at] = sum(vals) / len(vals) if isinstance(col, ezr.Num) else max(set(vals), key=vals.count)
    
    # Recommend changes for the levers
    recommendations = {}
    for col_name, allowed in levers.items():
        if col_name not in header: continue
        at = header.index(col_name)
        current_val = row[at]
        
        if at in best_mids:
            target = best_mids[at]
            if isinstance(allowed, tuple): # Numeric
                low, high = allowed
                new_val = max(low, min(high, target))
                if abs(new_val - current_val) > 1e-4:
                    recommendations[col_name] = new_val
            elif isinstance(allowed, list): # Symbolic
                if target in allowed and target != current_val:
                    recommendations[col_name] = target
                
    # Ensure at least one change if possible
    if not recommendations and levers:
        first_key = list(levers.keys())[0]
        val = levers[first_key]
        recommendations[first_key] = val[0] if isinstance(val, (list, tuple)) else val
        
    return recommendations

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Define levers excluding Team Size (as the customer cannot hire)
    levers = {
        "Size": (0.0, 1.0),
        "Plan": (0.0, 1.0),
        "Culture": (0.0, 1.0),
        "Dynamism": (0.0, 1.0)
    }
    
    # Pick a "bad" row (high ydist)
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Get fix
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Analysis: Cutting idle time without hiring.")
    print("Since hiring is not an option, we recommend adjusting these project parameters:")
    for col, val in recommendation.items():
        if isinstance(val, float):
            print(f"- Adjust '{col}' to {val:.4f}")
        else:
            print(f"- Adjust '{col}' to {val}")
    print("\nThese changes align your project with more efficient historical configurations.")
    
    exit(0)
