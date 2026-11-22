import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    A row is better if its goals (ending in - or +) are closer to their ideal.
    """
    # Create a table object using the provided data
    # We prepend the header to the rows to match the Tbl constructor expectation
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for every row. ydist measures how far a row's goals
    # are from the best possible values (0 for -, 1 for +).
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored_rows.append((d, i))
    
    # Sort by distance (ascending, so best first)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5%
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Found {len(best_indices)} top-performing setups out of {len(rows)}.")
    print("Indices of the best rows:")
    print(best_indices)
    
    # Show a sample of the best rows
    print("\nSample of top rows (Goal columns: Cost-, Score-, Idle-):")
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    for idx in best_indices[:3]:
        row = rows[idx]
        goals = [row[i] for i in goal_indices]
        print(f"Row {idx}: {goals}")
