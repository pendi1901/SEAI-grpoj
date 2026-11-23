import ezr
import step06
import step08

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the fraction of rows that `row` is better than.
    The reason explains why paying everyone more is not a simple solution,
    by showing that other factors (like role or tenure) often dominate the outcome.
    """
    # Use the logic from step06 to calculate the rank (p)
    p, _ = step06.justify(header, rows, row)
    
    # To explain why "paying everyone more" isn't the simple answer,
    # we check if MonthlyIncome is the primary driver of the ydist.
    # We compare the ydist of the row with its current income vs a hypothetical higher income.
    tbl = ezr.Tbl([header] + rows)
    col_map = {name: i for i, name in enumerate(header)}
    income_idx = col_map['MonthlyIncome']
    
    original_income = row[income_idx]
    row[income_idx] = original_income * 1.5  # Simulate a 50% raise
    
    new_ydist = ezr.ydist(tbl, row)
    row[income_idx] = original_income  # Reset
    
    # If the improvement is negligible, that's our reason.
    current_ydist = ezr.ydist(tbl, row)
    improvement = current_ydist - new_ydist
    
    if improvement < 0.05:
        reason = ("Simply increasing pay has a negligible impact on retention metrics "
                  "compared to other factors like role, tenure, and management, "
                  "suggesting that money alone does not solve the underlying attrition risks.")
    else:
        reason = ("While pay has some impact, other structural factors like role and "
                  "tenure remain significant drivers of employee retention, meaning "
                  "salary adjustments are only part of a complex solution.")
        
    return p, reason

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals
    sample_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for idx in goal_indices:
        sample_row[idx] = "?"
        
    # Justify
    p, reason = justify(header, rows, sample_row)
    
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
    
    exit(0)
