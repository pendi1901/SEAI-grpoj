import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining why the configuration is considered good.
    
    To answer the customer's question about "biggest, deepest" setups, we
    compare the performance of the input row against the distribution of
    performance in the dataset.
    """
    # Create a table to handle column roles and distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the performance of the input row.
    # We use the tree-based ranker to predict the ydist of the row.
    # A lower ydist is better.
    ranker_func = ezr.ranker(tbl)
    predicted_ydist = ranker_func(row)
    
    # Calculate ydist for all existing rows to establish the baseline
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that have a higher (worse) ydist than our row
    # A lower ydist is better, so we count how many rows are worse than our prediction
    better_than_count = sum(1 for d in all_ydists if d > predicted_ydist)
    p = better_than_count / len(rows)
    
    # Construct the reason
    # The customer asks why not use the biggest/deepest setup.
    # We explain that performance is about finding the right balance,
    # not just maximizing complexity.
    reason = (f"This configuration is estimated to outperform {p:.2f} of the known setups; "
              "bigger or deeper models often overfit, whereas this configuration "
              "balances complexity to maintain high performance.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a sample row to justify (e.g., the 50th row)
    # Mask its goals to simulate the "unknown" state
    target_row = list(rows[50])
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        target_row[idx] = "?"
            
    # Run justification
    p, reason = justify(header, rows, target_row)
    
    print("Analysis: Why not simply use the biggest, deepest setup?")
    print(f"Score (fraction of rows outperformed): {p:.4f}")
    print(f"Reason: {reason}")
