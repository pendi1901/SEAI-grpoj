import ezr
import step01

def remember(header, rows):
    """
    Finds the top 5% of rows that perform best across all goals.
    Uses the logic from step01 to identify the best configurations.
    """
    return step01.remember(header, rows)

def find_similar(header, rows, target_row, k=5):
    """
    Finds the k rows most similar to the target_row based on input (X) columns.
    """
    tbl = ezr.Tbl([header] + rows)
    # Calculate xdist between target_row and all other rows
    scored = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, target_row, row)
        scored.append((d, i))
    
    # Sort by distance (ascending, as lower distance means more similar)
    scored.sort(key=lambda x: x[0])
    return scored[:k]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    # Simulate a customer proposing a setup (using the first row as a sample)
    # We mask the goals to show we are treating it as a new proposal
    proposal = rows[0][:]
    for i, h in enumerate(header):
        if h[-1] in "+-":
            proposal[i] = "?"
            
    # Find similar past configurations
    similar = find_similar(header, rows, proposal)
    
    print("Customer Proposal Analysis:")
    print(f"Searching for past configurations similar to the proposal...")
    print(f"{'Rank':<6} | {'Row Index':<10} | {'Input Distance':<15} | {'Goal Distance (ydist)':<20}")
    print("-" * 60)
    
    tbl = ezr.Tbl([header] + rows)
    for rank, (dist, idx) in enumerate(similar):
        ydist = ezr.ydist(tbl, rows[idx])
        print(f"{rank+1:<6} | {idx:<10} | {dist:.4f}          | {ydist:.4f}")
        
    print("\nNote: Lower 'Goal Distance' indicates better performance.")
    exit(0)
