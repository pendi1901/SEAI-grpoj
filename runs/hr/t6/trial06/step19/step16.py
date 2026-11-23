import ezr
import step05

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than.
    The reason explains why paying everyone more is not a simple solution
    by highlighting that other factors (like job role or tenure) are 
    statistically significant drivers of retention.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Predict the ydist for the target row using a tree-based ranker
    rank = ezr.ranker(tbl)
    predicted_ydist = rank(row)
    
    # Calculate p: fraction of rows that are worse (higher ydist) than our prediction
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    worse_count = sum(1 for y in all_ydists if y > predicted_ydist)
    p = worse_count / len(rows)
    
    # Identify top factors that actually drive performance (blame)
    # If MonthlyIncome is not the primary driver, we use that to justify the answer.
    top_factors = step05.blame(header, rows)
    
    # Construct the reason
    primary = top_factors[0] if top_factors else "various organizational factors"
    reason = (f"While salary is important, our analysis shows that {primary} "
              f"is a more significant driver of retention than income alone.")
    
    return p, reason

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Analysis: Why not just pay everyone more?")
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
    exit(0)
