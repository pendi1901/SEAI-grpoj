import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows that perform best across all goals.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    # Create a table object to leverage ezr's normalization and distance logic
    # We construct the table by combining the header and the rows
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row. 
    # ydist in ezr calculates the distance from the ideal goal values.
    # Lower ydist means the row is closer to the optimal goals.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, as lower is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
    return [idx for _, idx in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
    print(f"{'Index':<10} | {'Cost-':<10} | {'Score-':<10} | {'Idle-':<10}")
    print("-" * 45)
    
    # Identify column indices for the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for idx in best_indices:
        row = rows[idx]
        goals = [f"{row[i]:.4f}" for i in goal_indices]
        print(f"{idx:<10} | {goals[0]:<10} | {goals[1]:<10} | {goals[2]:<10}")
