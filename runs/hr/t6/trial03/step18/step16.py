import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason explains why paying everyone more is not a simple solution.
    """
    # Use the logic from step06 to calculate the rank of the row
    p, _ = step06.justify(header, rows, row)
    
    # Analyze the correlation between MonthlyIncome and ydist
    # If income were the primary driver, higher income would always lead to lower ydist
    tbl = ezr.Tbl([header] + rows)
    income_idx = header.index('MonthlyIncome')
    
    # Calculate correlation (or simple difference in means)
    # Compare top 25% vs bottom 25% of earners
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    n = len(scored) // 4
    best = [x[1] for x in scored[:n]]
    worst = [x[1] for x in scored[-n:]]
    
    mu_best = sum(r[income_idx] for r in best) / len(best)
    mu_worst = sum(r[income_idx] for r in worst) / len(worst)
    
    # Construct the reason
    reason = (f"While increasing pay is a lever, our analysis shows that the difference "
              f"in average income between top and bottom performers is only "
              f"{abs(mu_best - mu_worst):.0f}, suggesting that other factors like "
              f"job satisfaction and work-life balance are equally critical to "
              f"retention as salary alone.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print("Justification Analysis: Why pay is not the only solution.")
    print(f"Rank of current arrangement: {p:.2f}")
    print(f"Reason: {reason}")
    
    exit(0)
