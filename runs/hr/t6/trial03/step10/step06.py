import ezr
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the ranking.
    """
    # Create a table to calculate ydist
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goal values for the target row using the tree-based ranker
    # We use the training data (rows) to build the model
    rank = step02.guess(header, rows, [row])
    
    # Fill the target row with estimated values to calculate its ydist
    # Goal indices are those ending in + or -
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    estimated_row = list(row)
    for i, idx in enumerate(goal_indices):
        estimated_row[idx] = rank[0]
        
    # Calculate ydist for the target row and all existing rows
    target_ydist = ezr.ydist(tbl, estimated_row)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that have a higher (worse) ydist than our target
    better_than = [y for y in all_ydists if y > target_ydist]
    p = len(better_than) / len(all_ydists)
    
    reason = (f"This arrangement ranks in the top {int((1-p)*100)}% of all records "
              f"because its predicted performance metrics are closer to the ideal "
              f"goals than {int(p*100)}% of the historical staff data.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print("Justification Analysis:")
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
    
    exit(0)
