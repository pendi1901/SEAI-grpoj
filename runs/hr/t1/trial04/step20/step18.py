import csv

def fix(header, row, levers):
    """
    Recommends changes to improve retention-related goals without increasing pay.
    Focuses on non-monetary levers: JobInvolvement, EnvironmentSatisfaction, 
    WorkLifeBalance, and TrainingTimesLastYear.
    """
    recommendations = {}
    
    # Map of column names to their indices
    col_map = {name: i for i, name in enumerate(header)}
    
    # Strategy:
    # 1. If 'WorkLifeBalance' is low (1 or 2), increase it to 3 or 4.
    # 2. If 'EnvironmentSatisfaction' is low (1 or 2), increase it to 3 or 4.
    # 3. If 'JobInvolvement' is low (1 or 2), increase it to 3 or 4.
    # 4. If 'TrainingTimesLastYear' is low, increase it.
    
    # We prioritize improving WorkLifeBalance and EnvironmentSatisfaction as they
    # are high-impact non-monetary factors.
    
    if 'WorkLifeBalance' in levers and 'WorkLifeBalance' in col_map:
        idx = col_map['WorkLifeBalance']
        low, high = levers['WorkLifeBalance']
        if row[idx] < 3:
            recommendations['WorkLifeBalance'] = min(high, 3.0)
            
    if 'EnvironmentSatisfaction' in levers and 'EnvironmentSatisfaction' in col_map:
        idx = col_map['EnvironmentSatisfaction']
        low, high = levers['EnvironmentSatisfaction']
        if row[idx] < 3:
            recommendations['EnvironmentSatisfaction'] = min(high, 4.0)
            
    if 'JobInvolvement' in levers and 'JobInvolvement' in col_map:
        idx = col_map['JobInvolvement']
        low, high = levers['JobInvolvement']
        if row[idx] < 3:
            recommendations['JobInvolvement'] = min(high, 3.0)

    # Fallback: If no specific improvement was triggered, pick the first available lever
    if not recommendations and levers:
        for col, val in levers.items():
            if isinstance(val, list):
                recommendations[col] = val[0]
            else:
                recommendations[col] = val[1]
                
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define non-monetary levers
    levers = {
        'WorkLifeBalance': (1.0, 4.0),
        'EnvironmentSatisfaction': (1.0, 4.0),
        'JobInvolvement': (1.0, 4.0),
        'TrainingTimesLastYear': (0.0, 6.0)
    }

    # Example: Fix the first row
    sample_row = rows[0]
    changes = fix(header, sample_row, levers)
    
    print("Non-monetary retention recommendations:")
    if not changes:
        print("No changes recommended for this employee.")
    else:
        for col, val in changes.items():
            print(f"- Increase {col} to {val}")
    
    print("\nConclusion: Since pay increases are not possible, we focus on improving "
          "work-life balance, environment, and job involvement to boost retention.")
