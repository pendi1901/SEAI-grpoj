import csv

def fix(header, row, levers):
    """
    Recommends changes for a 'bad' row (short tenure) to improve retention.
    We prioritize increasing pay-related metrics and reducing overtime.
    """
    recommendations = {}
    
    # Map indices for easier access
    idx_map = {h: i for i, h in enumerate(header)}
    
    # Strategy:
    # 1. If 'overTime' is 'Yes', change to 'No' (if allowed)
    if 'overTime' in levers and row[idx_map['overTime']] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            
    # 2. If 'PercentSalaryHike' is low (below 15%), increase it to the max allowed
    if 'PercentSalaryHike' in levers:
        low, high = levers['PercentSalaryHike']
        if row[idx_map['PercentSalaryHike']] < 15.0:
            recommendations['PercentSalaryHike'] = float(high)
            
    # 3. If 'StockOptionLevel' is low, increase it
    if 'StockOptionLevel' in levers:
        low, high = levers['StockOptionLevel']
        if row[idx_map['StockOptionLevel']] < high:
            recommendations['StockOptionLevel'] = float(high)
            
    # 4. If 'TrainingTimesLastYear' is low, increase it
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        if row[idx_map['TrainingTimesLastYear']] < 3:
            recommendations['TrainingTimesLastYear'] = float(high)

    # Ensure we return at least one change if possible
    if not recommendations and levers:
        # Default fallback: pick the first lever and set to max/first option
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
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Identify a 'bad' row (e.g., lowest tenure)
    years_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda x: x[years_idx])
    
    recommendations = fix(header, bad_row, levers)
    
    print("Retention Strategy for Short-Tenure Staff:")
    print(f"Original Tenure: {bad_row[years_idx]} years")
    print("Recommended Changes:")
    for col, val in recommendations.items():
        print(f"- Set {col} to {val}")
    print("\nBy reducing overtime and increasing investment in pay and training,")
    print("we aim to improve long-term employee retention.")
