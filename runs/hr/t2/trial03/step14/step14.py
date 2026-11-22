import csv
import math

def flow(header, row, seen):
    """
    Detects if a team's composition has drifted significantly from the 
    historical norm. We monitor the 'MonthlyIncome' and 'Age' as proxies 
    for team stability. If the current row's values are more than 2 
    standard deviations away from the mean of the 'seen' population, 
    we flag the team as having changed.
    """
    if len(seen) < 30:
        return False

    # Focus on key numeric indicators of team composition
    indicators = ['MonthlyIncome', 'Age']
    indices = [header.index(col) for col in indicators]
    
    for idx in indices:
        vals = [r[idx] for r in seen]
        mean = sum(vals) / len(vals)
        variance = sum((x - mean) ** 2 for x in vals) / len(vals)
        std = math.sqrt(variance)
        
        if std > 0:
            z_score = abs(row[idx] - mean) / std
            # If the new arrival is a significant outlier, flag the team
            if z_score > 2.0:
                return True
                
    return False

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    seen = []
    drift_count = 0
    for row in rows:
        if flow(header, row, seen):
            drift_count += 1
        seen.append(row)
    
    print("Analysis: Detecting team composition drift.")
    print(f"Detected {drift_count} instances where a new arrival significantly shifted the team profile.")
    print("Logic: Flagged arrivals that are > 2 standard deviations from the mean of 'MonthlyIncome' or 'Age' of the existing team.")
