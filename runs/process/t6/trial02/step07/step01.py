import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows that perform best across all goals.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    # Create a table object to use ezr's utility functions
    # We construct the input as [header] + rows
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # ydist calculates how far a row is from the ideal goal values
    # (0 for minimize, 1 for maximize). Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, as lower is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print a readable summary for the customer
    print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
    print("-" * 60)
    print(f"{'Index':<10} | {'Cost-':<10} | {'Score-':<10} | {'Idle-':<10}")
    print("-" * 60)
    
    # Identify goal columns
    goal_cols = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for idx in best_indices:
        row = rows[idx]
        goals = [f"{row[i]:.4f}" for i in goal_cols]
        print(f"{idx:<10} | {goals[0]:<10} | {goals[1]:<10} | {goals[2]:<10}")
        
    exit(0)
