import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    A row is better if its goals (ending in - or +) are closer to their ideal.
    """
    # Create a table object from the provided data
    # We prepend the header to the rows to match the Tbl constructor expectation
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row. 
    # ydist measures how far a row's goals are from the best possible values.
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, as lower is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5% of rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    # Extract header and rows
    header = next(data_gen)
    rows = list(data_gen)
    
    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
    print("-" * 40)
    print(f"{'Index':<10} | {'Cost-':<10} | {'Score-':<10} | {'Idle-':<10}")
    print("-" * 40)
    
    # Identify column indices for goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for idx in best_indices:
        row = rows[idx]
        goals = [f"{row[i]:.4f}" for i in goal_indices]
        print(f"{idx:<10} | {goals[0]:<10} | {goals[1]:<10} | {goals[2]:<10}")
    
    exit(0)
