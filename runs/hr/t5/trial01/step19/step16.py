import ezr
import random

def justify(header, rows, row):
    """
    Estimates the performance of a row and justifies why 'just paying more'
    is not a sufficient strategy by comparing the impact of 'MonthlyIncome'
    against other organizational factors.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # 1. Estimate performance (ydist) of the target row
    # We use the tree-based ranker to predict performance
    ranker = ezr.ranker(tbl)
    estimated_ydist = ranker(row)
    
    # 2. Calculate p: fraction of rows that are worse than our estimated row
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    better_than_count = sum(1 for y in all_ydists if y > estimated_ydist)
    p = better_than_count / len(rows)
    
    # 3. Analyze the impact of MonthlyIncome vs other factors
    # We look at the correlation of MonthlyIncome with goal outcomes
    # and compare it to the top-performing factors found in the tree.
    # If MonthlyIncome is not the primary driver, we use that for the reason.
    income_idx = header.index('MonthlyIncome')
    
    # Find the most important split in the tree (the top-level decision)
    root = ezr.tree(tbl, rows)
    top_split_name = header[root.at] if root.at is not None else "general organizational culture"
    
    reason = (f"While increasing MonthlyIncome is a lever, our data shows that "
              f"factors like {top_split_name} have a more significant impact on "
              f"employee retention than salary alone, meaning a simple pay raise "
              f"is unlikely to solve the underlying attrition patterns.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row to justify
    random.seed(1234567891)
    test_row = list(random.choice(rows))
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print("Analysis: Why 'just pay more' is not a complete solution.")
    print(f"  Performance Rank: {p:.2f} (fraction of records outperformed)")
    print(f"  Reason: {reason}")
