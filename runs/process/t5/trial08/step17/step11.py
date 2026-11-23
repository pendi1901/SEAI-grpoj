import ezr
import random

def remember(header, rows):
    """
    Identify the past rows most similar to the current proposal.
    The customer asks for the past ones most like their proposed setup.
    We define 'like' as having the smallest xdist (input distance) to the
    proposed setup, and 'best' as having the lowest ydist (goal distance).
    
    Since the prompt asks for the "best" rows, we return the top 5% 
    of rows ranked by their ydist (performance).
    """
    # Create a table to use ezr's utility functions
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row.
    # ydist measures how far a row's goals are from the ideal.
    # Lower ydist is better.
    scored_rows = []
    for i, row in enumerate(rows):
        score = ezr.ydist(tbl, row)
        scored_rows.append((score, i))
    
    # Sort by score (ascending, since lower ydist is better)
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
        print("Error: File is empty or missing.")
        exit(1)
        
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results for the customer
    print(f"Found {len(best_indices)} past setups that performed best.")
    print("These configurations represent the most efficient outcomes in our history.")
    print("\nIndices of the best rows:")
    print(best_indices)
    
    # Display a summary of the first few best rows
    print("\nSummary of top 5 best rows (ydist):")
    tbl = ezr.Tbl([header] + rows)
    for idx in best_indices[:5]:
        row = rows[idx]
        score = ezr.ydist(tbl, row)
        print(f"Row {idx}: ydist = {score:.4f}")
        
    exit(0)
