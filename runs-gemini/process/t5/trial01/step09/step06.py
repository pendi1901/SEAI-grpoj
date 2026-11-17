import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the justification.
    """
    # Create a table to calculate metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows in the dataset
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # To estimate the ydist of the input 'row', we use the tree-based ranker
    # which predicts the performance based on the leaf node's mean ydist.
    ranker_func = ezr.ranker(tbl)
    predicted_ydist = ranker_func(row)
    
    # Calculate what fraction of rows are worse than our predicted ydist
    # (i.e., have a higher ydist, since lower is better)
    better_than_count = sum(1 for d in all_ydists if d > predicted_ydist)
    p = better_than_count / len(rows)
    
    # Construct a human-readable reason
    reason = (f"This setup is estimated to be in the top {int((1-p)*100)}% "
              f"of all possible configurations based on its input characteristics.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    # Pick a sample row to justify (e.g., the 100th row)
    # Mask the goal columns to simulate the customer's request
    sample_row = rows[100][:]
    for i in range(-3, 0):
        sample_row[i] = "?"
        
    # Get justification
    p, reason = justify(header, rows, sample_row)
    
    print("Justification Analysis:")
    print(f"Rank: This setup is better than {p*100:.1f}% of all known configurations.")
    print(f"Reason: {reason}")
    
    exit(0)
