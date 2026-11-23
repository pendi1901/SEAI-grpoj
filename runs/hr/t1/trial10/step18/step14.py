import csv

def flow(header, row, seen):
    """
    Detects if a team (represented by the current row) looks 'unusual' 
    compared to the historical distribution of teams.
    
    We use the 'YearsAtCompany+' and 'YearsInCurrentRole+' as the primary 
    indicators of team stability. If the current row's values are 
    statistically distant (more than 2 standard deviations) from the 
    historical mean of 'seen' rows, we flag it as a shift in team composition.
    """
    if len(seen) < 30:
        return False

    yac_idx = header.index('YearsAtCompany+')
    yicr_idx = header.index('YearsInCurrentRole+')

    def get_stats(data, idx):
        vals = [r[idx] for r in data]
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        return mean, var ** 0.5

    yac_mean, yac_std = get_stats(seen, yac_idx)
    yicr_mean, yicr_std = get_stats(seen, yicr_idx)

    # Avoid division by zero if data is perfectly uniform
    yac_std = yac_std if yac_std > 0 else 1.0
    yicr_std = yicr_std if yicr_std > 0 else 1.0

    # Calculate Z-scores for the current row
    z_yac = abs(row[yac_idx] - yac_mean) / yac_std
    z_yicr = abs(row[yicr_idx] - yicr_mean) / yicr_std

    # If the current team is more than 2 standard deviations away from the mean,
    # it is considered an outlier/shift in team composition.
    if z_yac > 2.0 or z_yicr > 2.0:
        return True

    return False

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
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)

    print(f"Analysis complete. Processed {len(rows)} records.")
    print(f"Detected {anomalies} instances where the team composition shifted significantly.")
    print("Logic: Flagged records where tenure metrics deviated > 2 standard deviations from historical norms.")
