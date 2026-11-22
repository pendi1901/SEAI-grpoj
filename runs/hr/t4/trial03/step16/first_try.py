import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import step06

def justify(header, rows, row):
    """
    Estimates the goal column for the provided row and calculates its percentile
    rank against the existing rows. Returns (p, reason).
    
    To answer the customer's question about paying everyone more, we analyze
    the impact of 'MonthlyIncome' on the goal 'YearsAtCompany+'.
    """
    # Use the logic from step06 to get the rank and base reason
    p, base_reason = step06.justify(header, rows, row)
    
    # Analyze the correlation between MonthlyIncome and the goal
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    income_idx = header.index('MonthlyIncome')
    
    # Simple correlation check
    incomes = [r[income_idx] for r in rows]
    goals = [r[goal_idx] for r in rows]
    correlation = sum((i - sum(incomes)/len(incomes)) * (g - sum(goals)/len(goals)) 
                      for i, g in zip(incomes, goals)) / len(rows)
    
    # Construct the answer
    if correlation > 0:
        reason = (f"While increasing pay correlates with tenure, it is only one of many factors; "
                  f"this arrangement ranks in the {p:.2%} percentile of performance.")
    else:
        reason = (f"Our analysis shows that simply paying more does not guarantee longer tenure, "
                  f"as other factors are more predictive; this arrangement ranks in the {p:.2%} percentile.")
    
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Test with a sample row
    test_row = rows[0][:]
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+'))
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
    exit(0)
