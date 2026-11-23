import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a human-readable reason based on the model's prediction.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Train a ranker (tree) on all available data to estimate the goals
    # The ranker returns the mean ydist of the leaf the row falls into
    ranker = ezr.ranker(tbl)
    
    # Estimate the ydist for the target row
    # Since the row has '?' for goals, we use the ranker's prediction
    # which represents the expected performance based on input settings
    predicted_ydist = ranker(row)
    
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that have a higher (worse) ydist than our row
    # (i.e., our row is better than them)
    better_than = [y for y in all_ydists if y > predicted_ydist]
    p = len(better_than) / len(all_ydists)
    
    # Formulate the reason
    reason = (f"This configuration is estimated to be in the top {int((1-p)*100)}% "
              "of all possible setups based on its input parameters.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Pick a sample row to justify (e.g., the 10th row)
    # Mask its goals to simulate the "unknown" scenario
    target_row = rows[10][:]
    masked_row = ["?"] * 3 + target_row[3:]
    
    p, reason = justify(header, rows, masked_row)
    
    print(f"Justification Analysis:")
    print(f"Performance percentile: {p:.2f}")
    print(f"Reason: {reason}")
