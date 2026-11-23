import csv

def fix(header, row, levers):
    """
    Since there is no money for pay, we focus on non-monetary levers:
    1. Reducing OverTime (if possible).
    2. Adjusting TrainingTimesLastYear to improve engagement.
    3. Changing BusinessTravel to a less demanding frequency.
    """
    recommendations = {}
    idx_map = {name: i for i, name in enumerate(header)}

    # 1. If OverTime is a lever and currently 'Yes', switch to 'No'
    if 'overTime' in levers and row[idx_map['overTime']] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            return recommendations

    # 2. If BusinessTravel is a lever, try to reduce travel frequency
    # Hierarchy: Travel_Frequently -> Travel_Rarely -> Non-Travel
    if 'businessTravel' in levers:
        current_travel = row[idx_map['businessTravel']]
        if current_travel == 'Travel_Frequently' and 'Travel_Rarely' in levers['businessTravel']:
            recommendations['businessTravel'] = 'Travel_Rarely'
            return recommendations
        elif current_travel == 'Travel_Rarely' and 'Non-Travel' in levers['businessTravel']:
            recommendations['businessTravel'] = 'Non-Travel'
            return recommendations

    # 3. If TrainingTimesLastYear is a lever, aim for the middle-high range (e.g., 3-4)
    # to encourage professional growth without burnout.
    if 'TrainingTimesLastYear' in levers:
        low, high = levers['TrainingTimesLastYear']
        target = min(high, max(low, 3.0))
        if row[idx_map['TrainingTimesLastYear']] != target:
            recommendations['TrainingTimesLastYear'] = target
            return recommendations

    # Fallback: If no specific logic triggered, pick the first available lever
    for col, val in levers.items():
        if isinstance(val, list):
            recommendations[col] = val[0]
        else:
            recommendations[col] = val[0]
        break
            
    return recommendations

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0)
    }

    # Simulate fixing a 'bad' row (e.g., first row where attrition is 'Yes')
    bad_row = next((r for r in rows if r[header.index('attrition')] == 'Yes'), rows[0])
    
    changes = fix(header, bad_row, levers)
    
    print("Non-Monetary Retention Strategy:")
    print("Since budget is unavailable, we recommend the following adjustments to improve retention:")
    for col, val in changes.items():
        print(f"- Adjust '{col}' to: {val}")
    print("\nThese changes focus on reducing work-related stress and increasing professional development.")
