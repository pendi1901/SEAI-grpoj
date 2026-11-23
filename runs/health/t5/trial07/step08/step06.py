import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining why the configuration is considered good.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the input row using the tree-based ranker
    # We use the ranker logic from ezr to predict the performance of the row
    ranker_func = ezr.ranker(tbl)
    
    # Calculate the predicted ydist for the input row
    # Note: ranker returns the leaf's mean ydist, which is our estimate
    predicted_ydist = ranker_func(row)
    
    # Calculate ydist for all existing rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that have a higher (worse) ydist than our row
    # A lower ydist is better, so we count how many rows are worse than our prediction
    better_than_count = sum(1 for d in all_ydists if d > predicted_ydist)
    p = better_than_count / len(rows)
    
    # Construct the reason
    reason = (f"This configuration is estimated to outperform {int(p * 100)}% "
              "of the known setups based on its input parameters.")
    
    return p, reason

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a sample row to justify (e.g., the 10th row)
    # Mask its goals to simulate the "unknown" state
    target_row = list(rows[10])
    for i, name in enumerate(header):
        if name[-1] in "+-":
            target_row[i] = "?"
            
    # Run justification
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification Analysis:")
    print(f"Score: {p:.4f}")
    print(f"Reason: {reason}")
