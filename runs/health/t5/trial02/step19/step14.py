import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We stop if the current row is significantly better than the 
    best row seen so far, or if we have seen enough data to 
    conclude that further improvements are unlikely.
    """
    if not seen:
        return False
    
    # Create a table to handle column roles and ydist calculations
    # We use the header to define the structure
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the ydist of the current row and all seen rows
    current_ydist = ezr.ydist(tbl, row)
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Find the best performance seen so far
    best_so_far = min(seen_ydists)
    
    # Stop if we have seen at least 50 rows and the current row is 
    # not significantly better than the best we've already found.
    # This acts as an early stopping criterion.
    if len(seen) >= 50:
        # If the current row is worse than the best, and we have 
        # a decent sample size, we stop to save costs.
        if current_ydist >= best_so_far:
            return True
            
    return False

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopped at row {i+1}. The best setup has stopped improving.")
            print("Final selected setup details:")
            for h, v in zip(header, row):
                print(f"  {h}: {v}")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("Reached the end of the data without finding a stopping point.")
