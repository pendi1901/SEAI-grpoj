import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row (short tenure) to improve retention.
    We prioritize increasing pay (MonthlyIncome) and reducing overtime,
    as these are common drivers of attrition.
    """
    recommendations = {}
    
    # Map indices for easier access
    idx_map = {name: i for i, name in enumerate(header)}
    
    # 1. If 'overTime' is a lever and currently 'Yes', change to 'No'
    if 'overTime' in levers and row[idx_map['overTime']] == 'Yes':
        recommendations['overTime'] = 'No'
    
    # 2. If 'MonthlyIncome' is a lever, suggest an increase
    if 'MonthlyIncome' in levers:
        low, high = levers['MonthlyIncome']
        # Suggest a 10% increase, capped at the high limit
        current_income = row[idx_map['MonthlyIncome']]
        new_income = min(high, current_income * 1.10)
        recommendations['MonthlyIncome'] = new_income
        
    # 3. If 'TrainingTimesLastYear' is a lever, suggest increasing it
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        recommendations['TrainingTimesLastYear'] = high
        
    # 4. If 'StockOptionLevel' is a lever, suggest increasing it
    if 'StockOptionLevel' in levers:
        low, high = levers['StockOptionLevel']
        recommendations['StockOptionLevel'] = high

    # Ensure we return at least one recommendation
    if not recommendations and levers:
        # Fallback: pick the first lever and set to a reasonable value
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
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'MonthlyIncome': (1000.0, 20000.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Identify a 'bad' row (e.g., low tenure)
    idx_tenure = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[idx_tenure])
    
    changes = fix(header, bad_row, levers)
    
    print("Retention Strategy Recommendations for At-Risk Employees:")
    for col, val in changes.items():
        print(f"- Change '{col}' to: {val}")
    print("\nThese adjustments are designed to improve employee satisfaction and tenure.")
