import csv

def fix(header, row, levers):
    """
    Recommends changes to improve retention for a 'bad' row (low tenure)
    without using salary-based levers.
    
    We prioritize:
    1. Reducing OverTime (if 'No' is an option).
    2. Increasing TrainingTimesLastYear (to improve engagement).
    3. Adjusting BusinessTravel (to reduce stress).
    """
    recommendations = {}
    idx_map = {name: i for i, name in enumerate(header)}
    
    # 1. If OverTime is 'Yes', try to change to 'No'
    if 'overTime' in levers and row[idx_map['overTime']] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            
    # 2. If TrainingTimesLastYear is low, try to increase it
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        if row[idx_map['TrainingTimesLastYear']] < high:
            recommendations['TrainingTimesLastYear'] = high
            
    # 3. If BusinessTravel is frequent, try to reduce it
    if 'businessTravel' in levers and row[idx_map['businessTravel']] == 'Travel_Frequently':
        if 'Travel_Rarely' in levers['businessTravel']:
            recommendations['businessTravel'] = 'Travel_Rarely'
            
    # Fallback: If no specific logic triggered, pick the first available non-salary lever
    if not recommendations and levers:
        for col, val in levers.items():
            if col not in ['PercentSalaryHike', 'MonthlyIncome']:
                recommendations[col] = val[0] if isinstance(val, list) else val[1]
                break
                
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Levers excluding salary-based options
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Simulate a 'bad' row (e.g., low tenure)
    bad_row = rows[0]
    changes = fix(header, bad_row, levers)

    print("Retention Strategy Recommendations (Non-Monetary):")
    for col, val in changes.items():
        print(f"- Change '{col}' to: {val}")
    print("\nSince budget is constrained, we focus on work-life balance, "
          "professional development, and travel reduction to improve retention.")
