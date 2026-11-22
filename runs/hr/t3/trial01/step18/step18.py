import csv

def fix(header, row, levers):
    """
    Recommends changes for an employee who is likely to leave, 
    focusing on non-monetary levers (Work-Life Balance, Training, 
    Job Satisfaction, etc.) since there is no money for pay raises.
    """
    recommendations = {}
    
    # Priority 1: Reduce Overtime (if available)
    if 'overTime' in levers and row[header.index('overTime')] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            return recommendations

    # Priority 2: Adjust WorkLifeBalance (if available)
    # Assuming 1=Bad, 4=Excellent. If low, try to increase.
    if 'WorkLifeBalance' in levers:
        low, high = levers['WorkLifeBalance']
        if row[header.index('WorkLifeBalance')] < high:
            recommendations['WorkLifeBalance'] = float(high)
            return recommendations

    # Priority 3: Increase Training (if available)
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        if row[header.index('TrainingTimesLastYear')] < high:
            recommendations['TrainingTimesLastYear'] = float(high)
            return recommendations

    # Priority 4: Change Business Travel (if available)
    if 'businessTravel' in levers:
        if 'Non-Travel' in levers['businessTravel']:
            recommendations['businessTravel'] = 'Non-Travel'
            return recommendations

    # Fallback: If no specific logic triggered, pick the first available lever
    key = list(levers.keys())[0]
    val = levers[key]
    if isinstance(val, (list, tuple)):
        recommendations[key] = val[0] if isinstance(val, list) else val[1]
    else:
        recommendations[key] = val
        
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'WorkLifeBalance': (1.0, 4.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Example: Fix a row that works overtime
    sample_row = None
    for r in rows:
        if r[header.index('overTime')] == 'Yes':
            sample_row = r
            break
            
    if sample_row:
        changes = fix(header, sample_row, levers)
        print("Non-Monetary Retention Strategy:")
        for col, val in changes.items():
            print(f"- Change '{col}' to: {val}")
        print("\nLogic: Since budget is constrained, we prioritize reducing work-life stress "
              "and increasing professional development opportunities to improve retention.")
    else:
        print("No suitable records found for demonstration.")
