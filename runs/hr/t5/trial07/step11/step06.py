import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the ranking.
    """
    # Create a table to handle the data
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows in the dataset
    # Lower ydist is better.
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Estimate the ydist for the input row.
    # We use the tree-based ranker to predict the ydist of the input row
    # based on its input columns.
    ranker_func = ezr.ranker(tbl)
    predicted_ydist = ranker_func(row)
    
    # Calculate p: fraction of rows that are worse than our predicted row
    # A row is worse if its ydist is higher than our predicted ydist.
    worse_count = sum(1 for d in all_ydists if d > predicted_ydist)
    p = worse_count / len(rows)
    
    # Construct the reason
    reason = (f"This arrangement ranks in the top {int((1-p)*100)}% of all records "
              f"because its predicted performance distance of {predicted_ydist:.2f} "
              "is lower than the majority of observed staff outcomes.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals to test the function
    test_row = list(rows[0])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification Analysis:")
    print(f"  Rank (p): {p:.4f}")
    print(f"  Reason: {reason}")
    
    exit(0)
