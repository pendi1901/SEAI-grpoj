import csv
import random

def fix(header, row, levers):
    """
    Recommends changes for an employee who is likely to leave (a 'bad' row).
    We prioritize increasing 'MonthlyIncome' (if in levers) or adjusting 
    'OverTime'/'BusinessTravel' to improve retention.
    """
    recommendations = {}
    
    # Strategy: 
    # 1. If 'MonthlyIncome' is a lever, increase it to the high end.
    # 2. If 'overTime' is a lever, set it to 'No'.
    # 3. If 'businessTravel' is a lever, set it to 'Non-Travel'.
    
    if 'MonthlyIncome' in levers:
        low, high = levers['MonthlyIncome']
        recommendations['MonthlyIncome'] = high
    
    elif 'overTime' in levers:
        options = levers['overTime']
        if 'No' in options:
            recommendations['overTime'] = 'No'
            
    elif 'businessTravel' in levers:
        options = levers['businessTravel']
        if 'Non-Travel' in options:
            recommendations['businessTravel'] = 'Non-Travel'
            
    # Ensure at least one change is made if levers are provided
    if not recommendations and levers:
        key = list(levers.keys())[0]
        val = levers[key]
        recommendations[key] = val[0] if isinstance(val, (list, tuple)) else val
        
    return recommendations

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

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'MonthlyIncome': (1000.0, 20000.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Simulate fixing a 'bad' row (e.g., row 1 which has low satisfaction)
    bad_row = rows[1]
    changes = fix(header, bad_row, levers)

    print("Analysis: Recommended changes for retention:")
    for col, val in changes.items():
        print(f"- Change '{col}' to: {val}")
    
    print("\nLogic: We prioritize increasing compensation and reducing work-life stress (Overtime/Travel) to improve employee retention.")
