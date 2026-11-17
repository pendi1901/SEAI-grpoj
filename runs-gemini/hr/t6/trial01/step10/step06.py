import ezr

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining the ranking.
    """
    # Create a table to use the ydist function
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    # A row is better if its ydist is smaller (closer to ideal goals)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # We need to estimate the ydist for the target 'row'
    # Since goal cells are '?', we use the tree-based ranker from ezr
    # to estimate the expected ydist for this row.
    ranker = ezr.ranker(tbl)
    target_ydist = ranker(row)
    
    # Calculate how many rows are worse than our target
    # A row is worse if its ydist is greater than our target's ydist
    worse_count = sum(1 for d in all_ydists if d > target_ydist)
    p = worse_count / len(rows)
    
    reason = (f"This arrangement ranks in the top {int((1-p)*100)}% of all observed "
              f"employee records based on the predicted retention goals.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row to justify (e.g., the last one)
    # Mask the goals to simulate the "day one" scenario
    target_row = list(rows[-1])
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    for idx in goal_indices:
        target_row[idx] = "?"
        
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification Analysis:")
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
    
    exit(0)
