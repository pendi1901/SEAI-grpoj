import ezr
import step01

def flow(header, row, seen):
    """
    Warn the customer if a new row is 'bad'. 
    We define 'bad' as a row that is significantly worse than the 
    historical average of the 'seen' data.
    """
    if not seen:
        return False
    
    # Create a table to calculate ydist for the current row and the seen data
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the ydist of the current row
    # ydist measures how far a row is from the ideal (0 for -, 1 for +).
    # Higher ydist means worse performance.
    current_score = ezr.ydist(tbl, row)
    
    # Calculate the average ydist of all seen rows
    seen_scores = [ezr.ydist(tbl, r) for r in seen]
    avg_score = sum(seen_scores) / len(seen_scores)
    
    # If the current row is significantly worse than the average (e.g., 20% worse),
    # we flag it as 'bad' (True).
    return current_score > (avg_score * 1.2)

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival process
    seen = []
    warnings = 0
    
    for row in rows:
        if flow(header, row, seen):
            warnings += 1
        seen.append(row)
        
    print(f"Monitoring complete.")
    print(f"Total rows processed: {len(rows)}")
    print(f"Number of 'bad' setups detected: {warnings}")
    print("Decision logic: Flagged a setup if its performance (ydist) was 20% worse than the historical average.")
    
    exit(0)
