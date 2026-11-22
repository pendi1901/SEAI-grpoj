import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses ydist to measure distance from the ideal goal values.
    """
    # Create a table object using the ezr library
    # The first row of the data is the header, so we combine it with the rows
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    # ydist measures how far a row is from the ideal (0.0 for all goals)
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending, as lower ydist is better)
    scored.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5%
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
    print("Indices of the most trustworthy setups:")
    print(best_indices)
    
    # Show details of the top 3
    print("\nTop 3 setups (Goal values: MRE-, ACC+, PRED40+):")
    for idx in best_indices[:3]:
        row = rows[idx]
        # Extract goal columns (those ending in - or +)
        goals = [row[i] for i, name in enumerate(header) if name[-1] in "+-"]
        print(f"Row {idx}: {goals}")
    
    exit(0)
