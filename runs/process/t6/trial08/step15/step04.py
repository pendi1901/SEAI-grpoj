import ezr
import step01

def flow(header, row, seen):
    """
    Decide whether to approve a row on the spot.
    We approve if the row is among the top 5% of potential candidates 
    based on the distribution of rows seen so far.
    """
    if not seen:
        return False
    
    # Create a table from seen rows to establish the context of "good"
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the distance of the current row from the ideal
    current_dist = ezr.ydist(tbl, row)
    
    # Calculate distances for all seen rows
    seen_dists = [ezr.ydist(tbl, r) for r in seen]
    
    # We approve if the current row is better than the 95th percentile 
    # of what we have seen so far (i.e., in the top 5%)
    threshold = sorted(seen_dists)[max(0, int(len(seen_dists) * 0.05))]
    
    return current_dist <= threshold

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    approved = []
    seen = []
    
    for row in rows:
        if flow(header, row, seen):
            approved.append(row)
        seen.append(row)
        
    print(f"Processed {len(rows)} proposals.")
    print(f"Approved {len(approved)} proposals based on real-time evaluation.")
    
    if approved:
        print(f"Sample of approved row (first one): {approved[0]}")
