import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    A row is better if its goals (ending in - or +) are closer to their ideal.
    """
    # Create a table object using the provided data
    # The ezr.Tbl function expects an iterable of rows including the header
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row. 
    # ydist measures how far a row's goals are from the best possible values.
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        score = ezr.ydist(tbl, row)
        scored_rows.append((score, i))
    
    # Sort by score (ascending, since lower ydist is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5% of rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    # Load the data
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    
    # Extract header and rows
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Found {len(best_indices)} top-performing setups out of {len(rows)} total.")
    print("Indices of the best rows:")
    print(best_indices)
    
    # Display a sample of the best rows
    print("\nSample of best rows (Goal columns: Cost-, Score-, Idle-):")
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    for idx in best_indices[:3]:
        row = rows[idx]
        goals = [row[i] for i in goal_indices]
        print(f"Row {idx}: {goals}")
