import ezr
import step01

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the ranking.
    """
    # Create a table to handle normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all existing rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate ydist for the target row
    # Note: ezr.ydist handles "?" by ignoring them in the distance calculation
    target_ydist = ezr.ydist(tbl, row)
    
    # A row is better if its ydist is lower (closer to 0)
    # Count how many rows have a higher (worse) ydist than our target
    better_than_count = sum(1 for d in all_ydists if d > target_ydist)
    p = better_than_count / len(rows)
    
    # Construct the reason
    # Identify the goal columns to mention in the explanation
    goal_names = [name for name in header if name[-1] in "+-"]
    reason = (f"This setup is in the top {int((1-p)*100)}% of all configurations "
              f"because its projected performance across {', '.join(goal_names)} "
              "is closer to the ideal targets than most other options.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    file_path = "pom3a.train.csv"
    rows_iter = ezr.csv(file_path)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Pick a sample row to justify (e.g., the 100th row)
    # Mask its goal columns to simulate the "unknown" state
    target_row = list(all_rows[100])
    for i, name in enumerate(header):
        if name[-1] in "+-":
            target_row[i] = "?"
            
    # Get justification
    p, reason = justify(header, all_rows, target_row)
    
    print(f"Justification for row 100:")
    print(f"Rank: Better than {p:.1%} of all configurations.")
    print(f"Reason: {reason}")
    
    exit(0)
