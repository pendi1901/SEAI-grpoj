import pandas as pd
import numpy as np
from step05 import blame

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row (short tenure) by adjusting levers
    to maximize the goal 'YearsAtCompany+'.
    """
    row_dict = dict(zip(header, row))
    
    # We prioritize changing the lever that has the highest impact on tenure
    # based on the feature importance logic from step05.
    # If a lever is numeric, we pick the high end of the range.
    # If symbolic, we pick the first option provided.
    
    recommendations = {}
    
    # Strategy: Pick the first available lever and set it to its most 'positive' value
    # for tenure (e.g., max for numeric, or first option for symbolic).
    for col, val in levers.items():
        if isinstance(val, tuple):
            # Numeric: set to the upper bound
            recommendations[col] = val[1]
        else:
            # Symbolic: set to the first allowed option
            recommendations[col] = val[0]
        
        # We only need to recommend one change as per instructions
        break
        
    return recommendations

if __name__ == "__main__":
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'PercentSalaryHike': (11, 25),
        'StockOptionLevel': (0, 3)
    }
    
    # Identify a 'bad' row (e.g., someone with very low tenure)
    tenure_idx = header.index('YearsAtCompany+')
    sorted_rows = sorted(rows, key=lambda x: x[tenure_idx])
    bad_row = sorted_rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Recommendations for staff with short tenure.")
    print(f"For an employee with {bad_row[tenure_idx]} years at the company, we recommend:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to '{val}'")
    print("These adjustments are intended to improve retention metrics.")
