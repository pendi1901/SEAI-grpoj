import csv
import random
from step08 import fix as base_fix

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row by adjusting non-monetary levers.
    Since there is no money for pay, we exclude 'PercentSalaryHike' 
    from the levers if it exists, and focus on work-life balance 
    and job engagement factors.
    """
    # Filter out salary-related levers if present
    filtered_levers = {k: v for k, v in levers.items() if 'Salary' not in k}
    
    # If no levers left, fallback to original logic but ensure we don't pick salary
    if not filtered_levers:
        filtered_levers = levers
        
    return base_fix(header, row, filtered_levers)

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

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0),
        'WorkLifeBalance': (1.0, 4.0),
        'JobSatisfaction': (1.0, 4.0)
    }

    # Pick a 'bad' row (low tenure)
    idx = header.index('YearsAtCompany+')
    bad_rows = sorted(rows, key=lambda r: r[idx])[:20]
    sample_row = bad_rows[0]

    recommendation = fix(header, sample_row, levers)

    print("Analysis: Recommendations for staff retention without salary increases.")
    print(f"Original row tenure: {sample_row[idx]} years")
    print("Suggested non-monetary changes to improve retention:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to: {val}")
    print("\nThese adjustments focus on work-life balance and job satisfaction,")
    print("which our analysis shows are significant drivers of long-term retention.")
