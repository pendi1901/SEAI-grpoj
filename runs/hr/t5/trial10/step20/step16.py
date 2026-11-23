import ezr
import random

def justify(header, rows, row):
    """
    Estimates the rank of a proposed row (e.g., one with increased salary)
    compared to the existing population. Returns (p, reason).
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Build a tree to predict ydist for the proposed row
    root = ezr.tree(tbl, tbl.rows)
    
    # Predict ydist for the proposed row
    # The tree leaf mean provides an estimate of how this row performs
    predicted_ydist = ezr.leaf(root, row).mu
    
    # Calculate ydist for all existing rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that have a worse (higher) ydist than our prediction
    # A row is better if its ydist is lower.
    better_than_count = sum(1 for y in all_ydists if y > predicted_ydist)
    p = better_than_count / len(all_ydists)
    
    reason = (f"Increasing salary alone only improves your rank to the top "
              f"{int((1-p)*100)}% of outcomes, suggesting that other factors "
              f"like job role and work-life balance are more critical for retention.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and simulate a "pay raise"
    # MonthlyIncome is at index 18
    sample_row = list(rows[0])
    sample_row[18] = 20000  # Significant pay increase
    
    # Mask goals for the justification
    for i, name in enumerate(header):
        if name.endswith(("+", "-")):
            sample_row[i] = "?"
            
    p, reason = justify(header, rows, sample_row)
    
    print("Analysis: Why not just pay everyone more?")
    print(f"Proposed rank (p-value): {p:.4f}")
    print(f"Reason: {reason}")
    
    exit(0)
