import csv

def flow(header, row, seen):
    """
    Detects if a team's composition has shifted significantly from the norm.
    We monitor the 'MonthlyIncome' and 'TotalWorkingYears' as proxies for team 
    composition. If the current row's values deviate significantly (more than 
    2 standard deviations) from the running mean of the 'seen' data, we flag 
    the team as having changed.
    """
    if len(seen) < 30:
        return False

    # Focus on key numeric indicators of team composition
    indicators = ['MonthlyIncome', 'TotalWorkingYears']
    indices = [header.index(col) for col in indicators]
    
    for idx in indices:
        values = [r[idx] for r in seen]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        # If std_dev is 0, skip to avoid division issues
        if std_dev == 0:
            continue
            
        # If the current row is more than 2 standard deviations away, 
        # it suggests a shift in team composition
        if abs(row[idx] - mean) > (2 * std_dev):
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print("Team Composition Drift Analysis:")
    print(f"Total employees processed: {len(rows)}")
    print(f"Number of shifts in team composition detected: {anomalies}")
    print("Logic: A shift is flagged when incoming employee data (Income/Tenure) "
          "deviates significantly (2+ standard deviations) from the historical average.")
