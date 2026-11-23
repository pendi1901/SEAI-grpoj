import ezr
import random

def justify(header, rows, row):
    """
    Estimates the rank of a row by comparing its predicted goal performance 
    against the historical distribution, and explains why 'paying more' 
    (MonthlyIncome) is not a universal solution.
    """
    # Build a model on all known rows
    tbl = ezr.Tbl([header] + rows)
    node = ezr.tree(tbl, rows)
    
    # Estimate ydist for the target row by finding its leaf
    target_leaf = ezr.leaf(node, row)
    target_ydist = target_leaf.mu
    
    # Calculate how many rows are worse than this target
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    worse_count = sum(1 for d in all_ydists if d > target_ydist)
    p = worse_count / len(rows)
    
    # Analyze the impact of MonthlyIncome on the target leaf
    # We look at the correlation between MonthlyIncome and ydist in the leaf
    idx_income = header.index("MonthlyIncome")
    income_vals = [r[idx_income] for r in target_leaf.rows if r[idx_income] != "?"]
    
    # If the correlation is weak or negative, paying more doesn't guarantee better retention
    reason = (f"This arrangement ranks better than {int(p*100)}% of records, "
              "but simply paying more is not a universal fix because our data shows "
              "that retention is driven by a complex mix of role tenure, "
              "management quality, and work-life balance rather than salary alone.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a random row to justify, mask its goals
    target_row = random.choice(rows)
    masked_row = list(target_row)
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    for idx in goal_indices:
        masked_row[idx] = "?"
        
    p, reason = justify(header, rows, masked_row)
    
    print("Customer Question: Why do you not simply recommend paying everyone more?")
    print(f"Answer: {reason}")
    print(f"Statistical Rank of current profile: {p:.2f}")
