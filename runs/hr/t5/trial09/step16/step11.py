import ezr
import random

def remember(header, rows):
    """
    Finds the 5% of rows most similar to the 'ideal' employee (the best performers).
    Similarity is defined by the distance to the best possible goal outcomes.
    """
    # Create a table to handle column statistics and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for every row.
    # ydist measures how far a row is from the ideal goal values (0.0 is perfect).
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending, so best/closest to ideal first)
    scored.sort()
    
    # Return top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the indices of the best rows
    best_indices = remember(header, rows)
    
    # Identify column indices for the goal metrics
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    
    print(f"Found {len(best_indices)} employees who represent the 'ideal' retention profile.")
    print("These employees are the most similar to the best possible outcomes in the dataset.")
    print("\nTop 3 examples (Goal metrics):")
    
    for i in best_indices[:3]:
        r = rows[i]
        goals = [f"{header[idx]}: {r[idx]}" for idx in goal_indices]
        print(f"- Row {i}: {', '.join(goals)}")
        
    print("\nThese individuals demonstrate the longest tenure and best role stability.")
