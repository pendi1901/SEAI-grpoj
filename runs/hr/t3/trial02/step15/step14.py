import csv

def flow(header, row, seen):
    """
    Detects if a team's composition has drifted significantly from the 'normal'
    distribution of the seen data. We monitor the distribution of 'JobSatisfaction'
    and 'MonthlyIncome' using a simple threshold on the mean.
    
    Returns True if the current row causes the team's average for these metrics
    to deviate by more than 2 standard deviations from the historical mean.
    """
    if len(seen) < 30:
        return False

    # Identify indices
    sat_idx = header.index('JobSatisfaction')
    inc_idx = header.index('MonthlyIncome')
    
    # Calculate historical stats
    seen_sat = [r[sat_idx] for r in seen]
    seen_inc = [r[inc_idx] for r in seen]
    
    mean_sat = sum(seen_sat) / len(seen_sat)
    std_sat = (sum((x - mean_sat) ** 2 for x in seen_sat) / len(seen_sat)) ** 0.5
    
    mean_inc = sum(seen_inc) / len(seen_inc)
    std_inc = (sum((x - mean_inc) ** 2 for x in seen_inc) / len(seen_inc)) ** 0.5
    
    # Check if current row is an outlier (drift)
    # If the new row is significantly different, flag the team
    drift_sat = abs(row[sat_idx] - mean_sat) > (2 * std_sat) if std_sat > 0 else False
    drift_inc = abs(row[inc_idx] - mean_inc) > (2 * std_inc) if std_inc > 0 else False
    
    return drift_sat or drift_inc

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
    drift_events = 0
    for row in rows:
        if flow(header, row, seen):
            drift_events += 1
        seen.append(row)
    
    print("Analysis: Monitoring team composition drift.")
    print(f"Total rows processed: {len(rows)}")
    print(f"Number of times team composition drifted significantly: {drift_events}")
    print("Strategy: Flagged rows where JobSatisfaction or MonthlyIncome deviated ")
    print("by more than 2 standard deviations from the historical team average.")
