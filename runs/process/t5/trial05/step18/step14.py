import ezr
import random

def flow(header, row, seen):
    """
    Detects if a new row is significantly worse than the historical trend.
    We define 'bad' as a row whose ydist is significantly higher than the 
    moving average of the ydist of the last 50 rows seen.
    """
    if not seen:
        return False

    # Create a table to handle normalization and ydist calculations
    # We use the 'seen' rows to establish the current context
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for the new row
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate the moving average of ydist for the last 50 rows
    recent_rows = seen[-50:]
    recent_ydists = [ezr.ydist(tbl, r) for r in recent_rows]
    avg_ydist = sum(recent_ydists) / len(recent_ydists)
    
    # If the new row's ydist is significantly worse (e.g., 20% higher) 
    # than the recent average, we flag it as "going bad".
    if current_ydist > avg_ydist * 1.2:
        return True
    
    return False

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    all_rows = list(rows_gen)
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(all_rows)
    
    seen = []
    flagged = None
    
    # Process rows one by one
    for row in all_rows:
        if flow(header, row, seen):
            flagged = row
            break
        seen.append(row)
    
    if flagged:
        print("Alert: A performance degradation has been detected.")
        print(f"The following row is significantly worse than recent trends:")
        print(f"{flagged}")
    else:
        print("Monitoring complete: No significant performance degradation detected.")
