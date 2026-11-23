import ezr
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the estimate.
    """
    # 1. Estimate the goals for the input row
    # We use the logic from step02 (tree-based estimation)
    # We need to create a table from the full rows to build the model
    tbl = ezr.Tbl([header] + rows)
    
    # Predict the ydist of the input row using the ranker
    # The ranker returns a function that estimates ydist
    ranker_func = ezr.ranker(tbl)
    estimated_ydist = ranker_func(row)
    
    # 2. Calculate how many rows are worse than this estimate
    # A row is better if its ydist is smaller.
    # So, 'row' is better than any row where row_ydist > estimated_ydist
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    worse_count = sum(1 for y in all_ydists if y > estimated_ydist)
    p = worse_count / len(rows)
    
    reason = (f"Based on the project configuration, this setup is estimated to outperform "
              f"{int(p * 100)}% of all known historical configurations.")
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Pick a sample row to justify (e.g., the 100th row)
    # Mask its goals to simulate the "unknown" state
    target_row = list(rows[100])
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for idx in goal_indices:
        target_row[idx] = "?"
        
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification for configuration:")
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
