import ezr
import step01
import step08

def fix(header, row, levers):
    """
    Finds the best adjustment to the provided levers to minimize 'Idle-'.
    We look at the top 5% of rows (best performers) and find the 
    centroid of the levers within that group to suggest improvements.
    """
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    rows = data[1:]
    tbl = ezr.Tbl(data)
    
    # Identify best rows using step01 logic
    best_indices = step01.remember(header, rows)
    best_rows = [rows[i] for i in best_indices]
    
    recommendations = {}
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        col = tbl.cols[idx]
        
        if isinstance(col, ezr.Num):
            # Target the mean of the best rows for this numeric lever
            target = sum(r[idx] for r in best_rows) / len(best_rows)
            # Clamp to allowed range
            low, high = allowed
            recommendations[col_name] = max(low, min(high, target))
        else:
            # For symbolic, pick the most frequent value in the best rows
            counts = {}
            for r in best_rows:
                val = r[idx]
                counts[val] = counts.get(val, 0) + 1
            best_val = max(counts, key=counts.get)
            if best_val in allowed:
                recommendations[col_name] = best_val
                
    return recommendations

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers (excluding Team Size as per "not allowed to hire")
    # We can change Culture, Criticality, Criticality Modifier, Initial Known, 
    # Inter-Dependency, Dynamism, Size, Plan.
    levers = {
        "Culture": (0.0, 1.0),
        "Plan": (0.0, 1.0),
        "Dynamism": (0.0, 1.0)
    }
    
    # Pick a "bad" row (highest Idle-)
    idle_idx = header.index("Idle-")
    bad_row = max(rows, key=lambda r: r[idle_idx])
    
    # Get recommendation
    rec = fix(header, bad_row, levers)
    
    print("Optimization Analysis: How to reduce idle time without hiring.")
    print("To improve efficiency, consider the following adjustments to your project parameters:")
    for col, val in rec.items():
        print(f"  Adjust '{col}' to {val:.4f}")
    print("\nThese adjustments align your project configuration with the characteristics "
          "of our most efficient, low-idle-time projects.")
