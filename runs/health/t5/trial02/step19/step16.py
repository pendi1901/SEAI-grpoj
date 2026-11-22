import ezr
import random

def justify(header, rows, row):
    """
    Estimates the performance of a given setup and compares it to the 
    rest of the population to justify why 'bigger' isn't always 'better'.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Train a ranker to estimate the performance of the target row
    # The ranker uses a tree to find the leaf node and return the mean ydist
    ranker = ezr.ranker(tbl)
    
    # Estimate the performance of the target row
    estimated_ydist = ranker(row)
    
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that 'row' is better than.
    # A row is better if its ydist is lower.
    better_than_count = sum(1 for yd in all_ydists if yd > estimated_ydist)
    p = better_than_count / len(all_ydists)
    
    # Reason: Explain that bigger setups often increase complexity without 
    # guaranteeing better performance, as shown by the distribution.
    reason = (
        f"While larger setups increase model complexity, this configuration "
        f"is better than {int(p * 100)}% of all observed setups, suggesting "
        f"that adding more depth or estimators often yields diminishing returns."
    )
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Select a "big" setup to evaluate (e.g., high N_estimators, high depth)
    # We find the row with the highest N_estimators to represent a "big" setup
    n_est_idx = header.index("N_estimators")
    big_row = max(rows, key=lambda r: r[n_est_idx])
    
    # Mask the goals to simulate the "unknown" scenario
    target_row = list(big_row)
    for col in ezr.Tbl([header]).y:
        target_row[col.at] = "?"
        
    p, reason = justify(header, rows, target_row)
    
    print("Analysis: Why not use the biggest, deepest setup?")
    print(f"Performance percentile: {p:.2f}")
    print(f"Reason: {reason}")
