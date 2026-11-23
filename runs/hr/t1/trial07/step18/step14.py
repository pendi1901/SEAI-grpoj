import csv

def flow(header, row, seen):
    """
    Detects if the current row represents a 'drift' in team composition.
    We compare the current row's numeric distribution to the distribution
    of the 'seen' rows. If the current row's average numeric value is 
    statistically distant (e.g., > 2 standard deviations) from the 
    historical average of the team, we flag it as a change.
    """
    if len(seen) < 30:
        return False

    # Identify numeric columns
    numeric_indices = [i for i, h in enumerate(header) if h[0].isupper()]
    
    # Calculate historical means and standard deviations
    means = {}
    stds = {}
    for i in numeric_indices:
        vals = [r[i] for r in seen if isinstance(r[i], (int, float))]
        if len(vals) > 1:
            m = sum(vals) / len(vals)
            s = (sum((x - m) ** 2 for x in vals) / len(vals)) ** 0.5
            means[i] = m
            stds[i] = s if s > 0 else 1.0

    # Calculate Z-score for the current row
    z_scores = []
    for i in numeric_indices:
        if i in means and isinstance(row[i], (int, float)):
            z = abs(row[i] - means[i]) / stds[i]
            z_scores.append(z)
    
    # If the average Z-score across all numeric fields is high, 
    # the team composition has drifted significantly.
    if z_scores and (sum(z_scores) / len(z_scores)) > 2.5:
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
    flagged = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Team composition drift detected at record {i}.")
            flagged = True
            break
        seen.append(row)
    
    if not flagged:
        print("No significant team composition drift detected.")
