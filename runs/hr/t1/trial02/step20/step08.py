import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row (low tenure) to improve retention.
    We prioritize increasing pay (PercentSalaryHike), stock options, 
    and reducing overtime or travel frequency.
    """
    recommendations = {}
    
    # Map indices for quick lookup
    h_map = {name: i for i, name in enumerate(header)}
    
    # Strategy:
    # 1. If overtime is 'Yes' and we can change it, set to 'No'.
    if 'overTime' in levers and row[h_map['overTime']] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            
    # 2. If PercentSalaryHike is low, increase it to the max allowed.
    if 'PercentSalaryHike' in levers:
        low, high = levers['PercentSalaryHike']
        if row[h_map['PercentSalaryHike']] < high:
            recommendations['PercentSalaryHike'] = high
            
    # 3. If StockOptionLevel is low, increase it.
    if 'StockOptionLevel' in levers:
        low, high = levers['StockOptionLevel']
        if row[h_map['StockOptionLevel']] < high:
            recommendations['StockOptionLevel'] = high
            
    # 4. If businessTravel is high frequency, reduce it.
    if 'businessTravel' in levers and row[h_map['businessTravel']] == 'Travel_Frequently':
        if 'Travel_Rarely' in levers['businessTravel']:
            recommendations['businessTravel'] = 'Travel_Rarely'
            
    # Ensure at least one change is made if possible
    if not recommendations and levers:
        # Fallback: pick the first available lever and set to a reasonable value
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

    # Define available levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0),
        'TrainingTimesLastYear': (0.0, 6.0)
    }

    # Pick a sample 'bad' row (e.g., low tenure)
    yac_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[yac_idx])
    
    changes = fix(header, bad_row, levers)
    
    print("Retention Analysis for Short-Tenure Employee:")
    print(f"Current Tenure: {bad_row[yac_idx]} years")
    print("Recommended changes to improve retention:")
    for col, val in changes.items():
        print(f" - Change '{col}' to {val}")
