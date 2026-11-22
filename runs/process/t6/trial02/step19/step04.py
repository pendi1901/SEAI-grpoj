import ezr
import step01

def flow(header, row, seen):
    """
    Decide whether to approve a row immediately.
    We approve if the row is in the top 5% of the expected distribution
    based on the data seen so far.
    """
    if not seen:
        return False
    
    # Create a table from seen rows to understand the distribution
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # A row is "good" if its ydist is better than the current median ydist
    # of the rows we have already seen.
    current_ydists = [ezr.ydist(tbl, r) for r in seen]
    median_ydist = sorted(current_ydists)[len(current_ydists) // 2]
    
    # Calculate ydist for the new row
    new_ydist = ezr.ydist(tbl, row)
    
    # Approve if the new row is significantly better than the median
    # (i.e., in the top half of performance)
    return new_ydist < median_ydist

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    seen = []
    approved_count = 0
    
    for row in rows:
        if flow(header, row, seen):
            approved_count += 1
        seen.append(row)
        
    print(f"Processed {len(rows)} proposals.")
    print(f"Total approved: {approved_count}")
    print("Decision logic: Approved if row performance is better than the median of seen data.")
    
    exit(0)
