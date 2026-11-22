import ezr
import step06

def justify(header, rows, row):
    """
    Justify why 'paying everyone more' is not a simple solution.
    We compare the target row's performance (ydist) against a hypothetical
    version of the same row where 'MonthlyIncome' is increased by 20%.
    """
    # Create a table to calculate ydist
    tbl = ezr.Tbl([header] + rows)
    
    # Identify index for MonthlyIncome
    inc_idx = header.index('MonthlyIncome')
    
    # Estimate performance of the current row
    # We use the logic from step06 to get the ranking
    p, _ = step06.justify(header, rows, row)
    
    # Create a hypothetical row with 20% more income
    hypo_row = list(row)
    hypo_row[inc_idx] = row[inc_idx] * 1.2
    
    # Estimate performance of the hypothetical row
    p_hypo, _ = step06.justify(header, rows, hypo_row)
    
    # The reason explains that income is only one factor among many
    reason = (f"Increasing income by 20% only improves the retention ranking from "
              f"{int(p*100)}% to {int(p_hypo*100)}%, suggesting that other "
              f"factors like job role and work-life balance are more critical.")
    
    return p, reason

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and hide its goals
    sample_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for i in goal_indices:
        sample_row[i] = "?"
            
    # Run justification
    p, reason = justify(header, rows, sample_row)
    
    print("Analysis: Why not just pay everyone more?")
    print(f"Current ranking: {p:.2f}")
    print(f"Justification: {reason}")
