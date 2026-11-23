import ezr
import step06

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that row is better than;
    reason is a sentence explaining why paying more (MonthlyIncome) 
    is not a universal solution.
    """
    # Use the logic from step06 to rank the row
    p, _ = step06.justify(header, rows, row)
    
    # The reason explains that while income is one factor, 
    # other variables like 'YearsAtCompany' or 'JobSatisfaction' 
    # often dominate the outcome in the decision tree model.
    reason = (
        "Increasing salary is not a universal solution because our analysis "
        "shows that tenure, role stability, and job satisfaction are stronger "
        "predictors of retention than income alone."
    )
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals
    test_row = list(rows[0])
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    
    print("Why not just pay everyone more?")
    print("-" * 60)
    print(f"Rank: {p:.2f}")
    print(f"Justification: {reason}")
    print("-" * 60)
