import ezr
import random

def remember(header, rows):
    """
    Find the best-performing rows in the dataset.
    A row is better if its goals (ending in - or +) are closer to their ideal.
    We return the top 5% of rows based on their ydist score.
    """
    # Create a table object using the ezr library
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row.
    # ydist measures how far a row's goals are from the best possible values.
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        score = ezr.ydist(tbl, row)
        scored_rows.append((score, i))
    
    # Sort by score (ascending, as lower ydist is better)
    scored_rows.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40 rows)
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
        print("Error: File is empty.")
        exit(1)
        
    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print("Past setups most like the ideal:")
    print("-" * 40)
    print(f"{'Index':<10} | {'ydist':<10}")
    print("-" * 40)
    
    # Re-calculate ydist for display purposes
    tbl = ezr.Tbl([header] + rows)
    for idx in best_indices:
        score = ezr.ydist(tbl, rows[idx])
        print(f"{idx:<10} | {score:.4f}")
        
    print("-" * 40)
    print(f"Found {len(best_indices)} top-performing historical setups.")
    
    exit(0)
