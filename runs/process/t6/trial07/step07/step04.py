import ezr
import step01

def flow(header, row, seen):
    """
    Decide whether to approve a row on the spot.
    We approve if the row is in the top 5% of the expected distribution
    based on the data seen so far.
    """
    if not seen:
        return False
    
    # Create a table from seen rows to calculate ydist
    # We use the header to define the columns
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # Calculate ydist for the current row
    # Note: row might have '?' for goals, but ydist handles that via norm
    current_ydist = ezr.ydist(tbl, row)
    
    # We define "top 5%" as being better than the 5th percentile of seen rows
    seen_ydists.sort()
    threshold_idx = max(0, len(seen_ydists) // 20)
    threshold = seen_ydists[threshold_idx]
    
    # Approve if current row is better (lower ydist) than the threshold
    return current_ydist <= threshold

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    approved_count = 0
    seen = []
    
    # Simulate arrival one by one
    for row in rows:
        if flow(header, row, seen):
            approved_count += 1
        seen.append(row)
        
    print(f"Total rows processed: {len(rows)}")
    print(f"Total proposals approved: {approved_count}")
    print("Decision logic: Approved if row is in the top 5% of observed performance.")
    exit(0)
