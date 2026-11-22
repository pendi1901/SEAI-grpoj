import ezr
import step01

def flow(header, row, seen):
    """
    Decide whether to approve a row on the spot.
    We approve if the row is in the top 5% of the expected distribution
    based on the 'seen' data.
    """
    # If this is the first row, we have no context, so we let it go.
    if not seen:
        return False
    
    # Create a table from seen rows to understand the distribution
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the ydist of the current row
    # Note: row goals are not hidden in the input, so we can evaluate it directly
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows to establish a baseline
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # We define "top 5%" as being better than the 95th percentile of seen rows
    # Since lower ydist is better, we look for values in the bottom 5%
    seen_ydists.sort()
    threshold_idx = max(0, int(len(seen_ydists) * 0.05))
    threshold = seen_ydists[threshold_idx]
    
    # Approve if the current row is better than or equal to our threshold
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    approved = []
    seen = []
    
    for row in all_rows:
        if flow(header, row, seen):
            approved.append(row)
        seen.append(row)
        
    print(f"Processed {len(all_rows)} configurations.")
    print(f"Approved {len(approved)} configurations based on real-time criteria.")
    
    if approved:
        tbl = ezr.Tbl([header] + all_rows)
        avg_dist = sum(ezr.ydist(tbl, r) for r in approved) / len(approved)
        print(f"Average goal distance of approved items: {avg_dist:.4f}")
    
    exit(0)
