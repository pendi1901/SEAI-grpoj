import csv
import random

def fix(header, row, levers):
    """
    Suggests changes to a 'bad' row to improve its retention metrics.
    We prioritize changing levers that have the most positive impact on 
    the goal columns (YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+).
    """
    recommendations = {}
    
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Strategy: 
    # 1. If 'overTime' is a lever and currently 'Yes', change to 'No'.
    # 2. If 'PercentSalaryHike' is a lever, increase it towards the high end.
    # 3. If 'TrainingTimesLastYear' is a lever, increase it.
    # 4. If 'businessTravel' is a lever, change to 'Non-Travel'.
    
    if 'overTime' in levers and row[header.index('overTime')] == 'Yes':
        recommendations['overTime'] = 'No'
    
    if 'PercentSalaryHike' in levers:
        low, high = levers['PercentSalaryHike']
        recommendations['PercentSalaryHike'] = high
        
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        recommendations['TrainingTimesLastYear'] = high
        
    if 'businessTravel' in levers and row[header.index('businessTravel')] != 'Non-Travel':
        recommendations['businessTravel'] = 'Non-Travel'
        
    if 'StockOptionLevel' in levers:
        low, high = levers['StockOptionLevel']
        recommendations['StockOptionLevel'] = high

    # Ensure at least one change is made if possible
    if not recommendations and levers:
        first_key = list(levers.keys())[0]
        val = levers[first_key]
        recommendations[first_key] = val[1] if isinstance(val, tuple) else val[0]
        
    return recommendations

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Pick a 'bad' row (e.g., one with low tenure) to demonstrate
    idx_tenure = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[idx_tenure])
    
    changes = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for employees at risk of leaving:")
    for col, val in changes.items():
        print(f"- Change '{col}' to {val}")
    
    print("\nThese changes are designed to reduce burnout (overtime) and increase engagement (training/pay).")
