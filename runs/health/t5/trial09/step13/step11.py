import ezr
import random

def remember(header, rows):
    """
    Identify the top 5% of rows that are most similar to the 'ideal' 
    configuration (the one with the best possible ydist).
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for every row. Lower ydist is better.
    # ydist measures how far a row's goals are from the best they could be.
    scored_rows = []
    for i, row in enumerate(rows):
        scored_rows.append((i, ezr.ydist(tbl, row)))
    
    # Sort by ydist ascending (best first)
    scored_rows.sort(key=lambda x: x[1])
    
    # Return top 5% of rows (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[0] for item in scored_rows[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Get indices of best rows
    best_indices = remember(header, rows)
    
    # Print summary for the customer
    print(f"Analysis complete on {len(rows)} records.")
    print(f"Identified {len(best_indices)} setups most similar to the ideal configuration.")
    print("Indices of top-performing setups:")
    print(best_indices)
    
    # Show details of the very best one
    best_idx = best_indices[0]
    print(f"\nDetails of the top-ranked setup (Index {best_idx}):")
    for name, val in zip(header, rows[best_idx]):
        print(f"  {name}: {val}")
    
    exit(0)
