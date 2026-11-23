import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses the ydist metric from ezr to find rows closest to the ideal goals.
    """
    # Create a table object to leverage ezr's column and distance logic
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    # ydist measures how far a row's goals are from the best possible values
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending: lower is better)
    scored.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty.")
        exit(1)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print results
    print(f"Analysis complete. Found {len(best_indices)} top-performing configurations.")
    print("Indices of the most trustworthy setups (0-based):")
    print(best_indices)
    
    # Display a sample of the best rows
    print("\nTop 3 configurations:")
    for i in best_indices[:3]:
        print(f"Row {i}: {rows[i]}")
    
    exit(0)
