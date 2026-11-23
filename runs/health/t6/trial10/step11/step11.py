import ezr
import step01

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    Uses ydist to measure distance from the ideal goal values.
    """
    # Create a table object using the provided data
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row
    # A lower ydist means the row is closer to the ideal goals
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending)
    scored.sort(key=lambda x: x[0])
    
    # Return the top 5% of indices
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    header = all_rows[0]
    rows = all_rows[1:]
    
    # Get the best rows
    best_indices = remember(header, rows)
    
    # Print a summary for the customer
    print("Analysis complete. Here are the top performing setups:")
    print(f"{'Index':<10} | {'Y-Distance (Lower is better)':<30}")
    print("-" * 45)
    
    tbl = ezr.Tbl([header] + rows)
    for i in best_indices:
        d = ezr.ydist(tbl, rows[i])
        print(f"{i:<10} | {d:.4f}")
        
    print(f"\nFound {len(best_indices)} setups that are most like the ideal.")
