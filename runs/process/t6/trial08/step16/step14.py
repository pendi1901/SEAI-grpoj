import ezr
import step04

def flow(header, row, seen):
    """
    Warn the customer the moment a project setup starts to go bad.
    We define 'going bad' as the current row being significantly worse 
    than the historical performance of the project.
    
    We use the logic from step04 to determine if a row is 'approved' 
    (good). If it is NOT approved, we flag it as 'bad'.
    """
    # If we have no history, we cannot judge if it is bad.
    if not seen:
        return False
    
    # A row is 'good' if it is in the top 5% of potential candidates.
    # If it is NOT in the top 5%, it is considered 'bad' or 'going bad'.
    # We return True if the row is 'bad' (i.e., NOT approved).
    is_good = step04.flow(header, row, seen)
    
    return not is_good

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    bad_proposals = []
    seen = []
    
    for row in rows:
        if flow(header, row, seen):
            bad_proposals.append(row)
        seen.append(row)
        
    print(f"Processed {len(rows)} proposals.")
    print(f"Detected {len(bad_proposals)} setups that were flagged as 'going bad'.")
    
    if bad_proposals:
        print(f"The first flagged setup was at index {rows.index(bad_proposals[0])}.")
        print(f"Values: {bad_proposals[0]}")
    
    exit(0)
