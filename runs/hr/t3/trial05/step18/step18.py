import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row (short tenure) to improve retention
    without using salary (MonthlyIncome) as a lever.
    """
    recommendations = {}
    idx_map = {name: i for i, name in enumerate(header)}
    
    # 1. If 'overTime' is a lever and currently 'Yes', change to 'No'
    if 'overTime' in levers and row[idx_map['overTime']] == 'Yes':
        recommendations['overTime'] = 'No'
    
    # 2. If 'WorkLifeBalance' is a lever, suggest the highest value (4.0)
    if 'WorkLifeBalance' in levers:
        low, high = levers['WorkLifeBalance']
        recommendations['WorkLifeBalance'] = high
        
    # 3. If 'TrainingTimesLastYear' is a lever, suggest increasing it
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        recommendations['TrainingTimesLastYear'] = high
        
    # 4. If 'StockOptionLevel' is a lever, suggest increasing it
    if 'StockOptionLevel' in levers:
        low, high = levers['StockOptionLevel']
        recommendations['StockOptionLevel'] = high

    # Fallback: if no specific logic triggered, pick the first available lever
    if not recommendations and levers:
        first_key = list(levers.keys())[0]
        val = levers[first_key]
        recommendations[first_key] = val[1] if isinstance(val, (tuple, list)) else val[0]
        
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

    # Define levers excluding MonthlyIncome (no money for pay)
    levers = {
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0),
        'WorkLifeBalance': (1.0, 4.0)
    }

    # Identify a 'bad' row (e.g., low tenure)
    idx_tenure = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[idx_tenure])
    
    changes = fix(header, bad_row, levers)
    
    print("Retention Strategy Recommendations (No Salary Increases):")
    for col, val in changes.items():
        print(f"- Change '{col}' to: {val}")
    print("\nLogic: Since budget is constrained, we focus on non-monetary levers "
          "like reducing overtime, improving work-life balance, and increasing "
          "training and stock options to boost retention.")
