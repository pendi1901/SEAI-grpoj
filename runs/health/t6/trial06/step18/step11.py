import ezr
import step01
import step09

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    We use the ydist metric to find rows closest to the ideal goals.
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
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
        
        # Get the best rows
        best_indices = remember(header, rows)
        
        # Calculate table for ydist context
        tbl = ezr.Tbl([header] + rows)
        
        print(f"Analysis complete. Found {len(best_indices)} top-performing configurations.")
        print("The following setups are the most similar to the ideal goal (lowest ydist):")
        
        for i in best_indices[:5]:
            row = rows[i]
            score = ezr.ydist(tbl, row)
            print(f"Index {i:3}: ydist={score:.4f} | {row}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    exit(0)
