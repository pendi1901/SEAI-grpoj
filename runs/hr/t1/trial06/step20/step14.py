import csv

def flow(header, row, seen):
    """
    Detects if a team's composition has drifted significantly from the 
    historical baseline. We monitor the average 'JobSatisfaction' and 
    'TotalWorkingYears'. If the current row deviates significantly 
    (more than 2 standard deviations) from the moving average of the 
    'seen' population, we flag it as a potential shift in team dynamics.
    """
    if len(seen) < 50:
        return False

    idx_sat = header.index('JobSatisfaction')
    idx_exp = header.index('TotalWorkingYears')

    def get_stats(data, idx):
        vals = [r[idx] for r in data]
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        return mean, var ** 0.5

    mean_sat, std_sat = get_stats(seen, idx_sat)
    mean_exp, std_exp = get_stats(seen, idx_exp)

    # Flag if the new row is an outlier (beyond 2 standard deviations)
    # in either satisfaction or experience.
    is_outlier_sat = abs(row[idx_sat] - mean_sat) > (2 * std_sat) if std_sat > 0 else False
    is_outlier_exp = abs(row[idx_exp] - mean_exp) > (2 * std_exp) if std_exp > 0 else False

    return is_outlier_sat or is_outlier_exp

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
    drift_detected = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Drift detected at row {i}: The team composition has shifted significantly.")
            drift_detected = True
            break
        seen.append(row)

    if not drift_detected:
        print("No significant team composition drift detected.")
