import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a one-sentence explanation.
    """
    # Create a table to handle the data and distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # To estimate the goals of 'row', we use a tree-based ranker
    # The ranker predicts the ydist (distance to ideal) for any given row
    ranker = ezr.ranker(tbl)
    
    # Estimate the performance of the provided row
    # We use the ranker to predict its ydist
    predicted_ydist = ranker(row)
    
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate how many rows are worse than our predicted row
    # A row is better if its ydist is lower (closer to 0)
    # So, our row is better than any row with a higher ydist
    better_than_count = sum(1 for y in all_ydists if y > predicted_ydist)
    p = better_than_count / len(rows)
    
    reason = (f"This configuration is estimated to outperform {int(p * 100)}% "
              "of all known setups based on its input settings.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a sample row to justify (e.g., the 10th row)
    # Mask its goal columns to simulate the "unknown" state
    sample_row = list(rows[9])
    for i, name in enumerate(header):
        if name[-1] in "+-":
            sample_row[i] = "?"
            
    p, reason = justify(header, rows, sample_row)
    
    print(f"Justification Analysis:")
    print(f"Score (p): {p:.4f}")
    print(f"Reason: {reason}")
    
    exit(0)
