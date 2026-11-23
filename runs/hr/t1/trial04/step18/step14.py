import csv

def flow(header, row, seen):
    """
    Detects if a team's composition has drifted significantly from the historical
    norm. We monitor the distribution of 'JobSatisfaction' and 'TotalWorkingYears'.
    If the current row's values are outside the expected range (e.g., 2 standard 
    deviations from the mean of seen rows), we flag the team as 'changed'.
    """
    if not seen:
        return False

    # Identify indices for monitoring
    try:
        sat_idx = header.index('JobSatisfaction')
        tenure_idx = header.index('TotalWorkingYears')
    except ValueError:
        return False

    # Calculate stats from seen data
    sats = [s[sat_idx] for s in seen if isinstance(s[sat_idx], (int, float))]
    tenures = [s[tenure_idx] for s in seen if isinstance(s[tenure_idx], (int, float))]

    if len(sats) < 10:
        return False

    def get_z(val, data):
        mean = sum(data) / len(data)
        var = sum((x - mean) ** 2 for x in data) / len(data)
        std = var ** 0.5
        if std == 0:
            return 0
        return abs(val - mean) / std

    # Flag if the new row is a significant outlier in either metric
    z_sat = get_z(row[sat_idx], sats)
    z_tenure = get_z(row[tenure_idx], tenures)

    # If the new arrival is more than 2 standard deviations away, 
    # the team composition is no longer "normal".
    return z_sat > 2.0 or z_tenure > 2.0

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

    seen = []
    drift_count = 0
    for row in rows:
        if flow(header, row, seen):
            drift_count += 1
        seen.append(row)

    print("Analysis: Monitoring team composition drift.")
    print(f"Total records processed: {len(rows)}")
    print(f"Instances where team composition deviated from historical norms: {drift_count}")
    print("Conclusion: When the count of deviations is high, the team's profile has shifted significantly.")
