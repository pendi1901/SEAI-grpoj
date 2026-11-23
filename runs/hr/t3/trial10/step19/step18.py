import csv

def fix(header, row, levers):
    """
    Recommends non-monetary changes to improve retention for a 'bad' row.
    Since pay is fixed, we focus on work-life balance, job involvement, 
    and professional development levers.
    """
    recommendations = {}
    idx_map = {h: i for i, h in enumerate(header)}
    
    # Strategy:
    # 1. Reduce overtime if possible (High impact on burnout)
    if 'overTime' in levers and row[idx_map['overTime']] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            
    # 2. Increase JobInvolvement (Engagement)
    if 'JobInvolvement' in levers:
        low, high = levers['JobInvolvement']
        if row[idx_map['JobInvolvement']] < high:
            recommendations['JobInvolvement'] = float(high)
            
    # 3. Increase Training (Professional growth)
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        if row[idx_map['TrainingTimesLastYear']] < high:
            recommendations['TrainingTimesLastYear'] = float(high)
            
    # 4. Adjust WorkLifeBalance (if available)
    if 'WorkLifeBalance' in levers:
        low, high = levers['WorkLifeBalance']
        if row[idx_map['WorkLifeBalance']] < high:
            recommendations['WorkLifeBalance'] = float(high)

    # Fallback: If no specific logic triggered, pick a safe non-monetary change
    if not recommendations and levers:
        for key, val in levers.items():
            if key not in ['MonthlyIncome', 'PercentSalaryHike', 'StockOptionLevel']:
                recommendations[key] = val[1] if isinstance(val, tuple) else val[0]
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

    # Define non-monetary levers
    levers = {
        'overTime': ['No', 'Yes'],
        'JobInvolvement': (1.0, 4.0),
        'TrainingTimesLastYear': (0.0, 6.0),
        'WorkLifeBalance': (1.0, 4.0),
        'EnvironmentSatisfaction': (1.0, 4.0)
    }

    # Identify a 'bad' row (lowest tenure)
    years_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda x: x[years_idx])
    
    recommendations = fix(header, bad_row, levers)
    
    print("Retention Strategy (Non-Monetary):")
    print(f"Original Tenure: {bad_row[years_idx]} years")
    print("Recommended changes to improve retention without increasing pay:")
    for col, val in recommendations.items():
        print(f"- Set {col} to {val}")
    print("\nBy focusing on work-life balance, training, and engagement,")
    print("we can improve retention even when salary budgets are frozen.")
