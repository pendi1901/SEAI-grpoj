import csv

def fix(header, row, levers):
    """
    Recommends changes to non-monetary levers to improve an employee's tenure (YearsAtCompany+).
    Since pay is fixed, we focus on work-life balance and professional development.
    """
    recommendations = {}
    
    # Identify indices
    ot_idx = header.index('overTime')
    wlb_idx = header.index('WorkLifeBalance')
    train_idx = header.index('TrainingTimesLastYear')
    
    # Strategy:
    # 1. If Overtime is 'Yes', change to 'No' (if allowed)
    # 2. If WorkLifeBalance is low (1 or 2), try to increase it (if allowed)
    # 3. If TrainingTimesLastYear is low, increase it (if allowed)
    
    if 'overTime' in levers and row[ot_idx] == 'Yes':
        recommendations['overTime'] = 'No'
        
    elif 'WorkLifeBalance' in levers:
        # If we can't change overtime, try to improve WorkLifeBalance
        low, high = levers['WorkLifeBalance']
        recommendations['WorkLifeBalance'] = float(high)
        
    elif 'TrainingTimesLastYear' in levers:
        # If other options are exhausted, increase training
        low, high = levers['TrainingTimesLastYear']
        recommendations['TrainingTimesLastYear'] = float(high)
        
    # Fallback: if none of the above, pick the first available lever
    if not recommendations:
        for col, val in levers.items():
            if isinstance(val, list):
                recommendations[col] = val[0]
            else:
                recommendations[col] = float(val[1])
            break
            
    return recommendations

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define non-monetary levers
    levers = {
        'overTime': ['No', 'Yes'],
        'WorkLifeBalance': (1.0, 4.0),
        'TrainingTimesLastYear': (0.0, 6.0),
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']
    }

    # Find a 'bad' row (e.g., lowest tenure) to demonstrate
    tenure_idx = header.index('YearsAtCompany+')
    sorted_rows = sorted(rows, key=lambda r: r[tenure_idx])
    bad_row = sorted_rows[0]
    
    changes = fix(header, bad_row, levers)
    
    print("Retention Strategy (Non-Monetary):")
    for col, val in changes.items():
        print(f"- Change '{col}' to: {val}")
    print("\nSince budget is constrained, we recommend focusing on reducing overtime and increasing professional development to improve employee retention.")
