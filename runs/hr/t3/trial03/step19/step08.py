import csv
import random

def fix(header, row, levers):
    """
    Recommends changes for a 'bad' row (short tenure) to improve retention.
    We prioritize increasing 'PercentSalaryHike' or 'StockOptionLevel'
    and reducing 'overTime' or 'businessTravel' frequency.
    """
    recommendations = {}
    
    # Strategy:
    # 1. If 'overTime' is 'Yes', change to 'No' if allowed.
    # 2. If 'PercentSalaryHike' is low, increase it.
    # 3. If 'StockOptionLevel' is low, increase it.
    
    if 'overTime' in levers and row[header.index('overTime')] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            return recommendations

    if 'PercentSalaryHike' in levers:
        low, high = levers['PercentSalaryHike']
        current = row[header.index('PercentSalaryHike')]
        if current < high:
            recommendations['PercentSalaryHike'] = min(high, current + 5.0)
            return recommendations

    if 'StockOptionLevel' in levers:
        low, high = levers['StockOptionLevel']
        current = row[header.index('StockOptionLevel')]
        if current < high:
            recommendations['StockOptionLevel'] = min(high, current + 1.0)
            return recommendations

    # Default: pick first available lever and set to a reasonable value
    for col, val in levers.items():
        if isinstance(val, list):
            recommendations[col] = val[0]
        else:
            recommendations[col] = val[1]
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Simulate a 'bad' row (short tenure)
    # Finding a row with low YearsAtCompany+
    idx_years = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[idx_years])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Request: How to improve retention for short-tenure staff?")
    print(f"Recommended changes for employee (Current YearsAtCompany: {bad_row[idx_years]}):")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to: {val}")
    
    print("\nBy adjusting these levers, we aim to increase job satisfaction and tenure.")
