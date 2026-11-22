import ezr
import step01

def remember(header, rows):
    """
    Finds the top 5% of rows that are most similar to the 'best' 
    configurations found in the dataset.
    """
    # Create a table to calculate ydist (goal distance)
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for i, row in enumerate(rows):
        # We assume rows have goals. If they are '?', we use the model's 
        # prediction or skip. Given the context, we assume we can evaluate 
        # the rows provided.
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending, as lower is better)
    scored.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Get the indices of the best rows
    best_indices = remember(header, rows)
    
    print("Analysis: Past configurations most similar to the ideal:")
    print(f"Found {len(best_indices)} top-performing historical setups.")
    
    # Display a few of the best rows
    tbl = ezr.Tbl([header] + rows)
    print(f"{'Index':<10} | {'Goal Distance (ydist)':<20}")
    for idx in best_indices[:5]:
        dist = ezr.ydist(tbl, rows[idx])
        print(f"{idx:<10} | {dist:.4f}")
        
    print("\nThese configurations represent the 'gold standard' in our history.")
    exit(0)
