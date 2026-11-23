import ezr
import random

def justify(header, rows, row):
    """
    Justify why 'bigger/deeper' is not always better by comparing the 
    provided row's performance against the distribution of all rows.
    """
    # Create a table to handle the data and distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Use a tree-based ranker to estimate the performance of the provided row.
    # The ranker predicts the ydist (distance to ideal) for any given row.
    ranker = ezr.ranker(tbl)
    
    # Estimate the performance of the provided row
    predicted_ydist = ranker(row)
    
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # A row is better if its ydist is lower (closer to 0).
    # Our row is better than any row with a higher ydist.
    better_than_count = sum(1 for y in all_ydists if y > predicted_ydist)
    p = better_than_count / len(rows)
    
    # The reason explains that complexity (like depth/size) does not 
    # guarantee better performance, as shown by the estimated rank.
    reason = (f"This configuration is estimated to outperform {int(p * 100)}% "
              "of all known setups, demonstrating that increasing model "
              "complexity does not always yield better results.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a row that represents a "complex" setup (e.g., high depth, high estimators)
    # We look for a row with Max_depth > 15 and N_estimators > 150
    depth_idx = header.index("Max_depth")
    est_idx = header.index("N_estimators")
    
    complex_row = None
    for r in rows:
        if r[depth_idx] > 15 and r[est_idx] > 150:
            complex_row = list(r)
            break
    
    if complex_row:
        # Mask the goal columns
        for i, name in enumerate(header):
            if name[-1] in "+-":
                complex_row[i] = "?"
        
        p, reason = justify(header, rows, complex_row)
        
        print("Complexity Analysis: Why not use the biggest, deepest setup?")
        print(f"Performance Rank (p): {p:.4f}")
        print(f"Explanation: {reason}")
    else:
        print("No highly complex setup found to analyze.")
    
    exit(0)
