import ezr
import random

def remember(header, rows):
    """
    Finds the 5% of rows most similar to a target employee (the first row).
    Similarity is based on xdist (distance across input columns).
    """
    # Create a table to handle column definitions and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Target is the first row
    target = rows[0]
    
    # Calculate distance from target for all rows
    # We use xdist to compare input columns
    distances = []
    for i, row in enumerate(rows):
        # Skip comparing the target to itself
        if i == 0:
            continue
        d = ezr.xdist(tbl, row, target)
        distances.append((d, i))
    
    # Sort by distance (lower is more similar)
    distances.sort()
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
    return [i for d, i in distances[:limit]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify goal columns for reporting
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    
    # Get indices of most similar employees
    similar_indices = remember(header, rows)
    
    print(f"Analysis: Found {len(similar_indices)} employees most similar to the target (Row 0).")
    print(f"Target row goals: {[rows[0][i] for i in goal_indices]}")
    print("\nTop similar employees and their goal outcomes:")
    
    for idx in similar_indices:
        outcomes = [f"{header[i]}: {rows[idx][i]}" for i in goal_indices]
        print(f"  Row {idx}: {', '.join(outcomes)}")
        
    print("\nMethodology: Used xdist to calculate similarity across all input columns,")
    print("then selected the 5% of records with the smallest distance to the target.")
    
    exit(0)
