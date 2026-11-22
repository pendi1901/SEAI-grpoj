import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row (low tenure) to improve retention
    without using salary-based levers.
    """
    recommendations = {}
    h_map = {name: i for i, name in enumerate(header)}
    
    # Strategy:
    # 1. Reduce overtime if possible.
    if 'overTime' in levers and row[h_map['overTime']] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            
    # 2. Increase StockOptionLevel if possible.
    if 'StockOptionLevel' in levers:
        low, high = levers['StockOptionLevel']
        if row[h_map['StockOptionLevel']] < high:
            recommendations['StockOptionLevel'] = high
            
    # 3. Increase training frequency to improve engagement.
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        if row[h_map['TrainingTimesLastYear']] < high:
            recommendations['TrainingTimesLastYear'] = high
            
    # 4. Reduce travel frequency if it's high.
    if 'businessTravel' in levers and row[h_map['businessTravel']] == 'Travel_Frequently':
        if 'Travel_Rarely' in levers['businessTravel']:
            recommendations['businessTravel'] = 'Travel_Rarely'
            
    # Fallback: if no specific logic triggered, pick the first available lever
    if not recommendations and levers:
        first_key = list(levers.keys())[0]
        val = levers[first_key]
        recommendations[first_key] = val[0] if isinstance(val, list) else val[1]
        
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

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'StockOptionLevel': (0.0, 3.0),
        'TrainingTimesLastYear': (0.0, 6.0)
    }

    # Pick a sample 'bad' row (e.g., lowest tenure)
    yac_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[yac_idx])
    
    changes = fix(header, bad_row, levers)
    
    print("Retention Analysis (No Budget for Salary Increases):")
    print(f"Current Tenure: {bad_row[yac_idx]} years")
    print("Recommended non-monetary changes to improve retention:")
    for col, val in changes.items():
        print(f" - Change '{col}' to {val}")
