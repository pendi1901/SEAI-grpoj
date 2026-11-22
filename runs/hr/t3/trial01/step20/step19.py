import csv

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' by measuring 
    the distance of each row from the centroid of the existing population.
    Rows with high distance are outliers and their estimates cannot be trusted.
    """
    # Identify numeric columns for distance calculation
    num_indices = [i for i, h in enumerate(header) if h[0].isupper()]
    
    # Calculate mean and std for each numeric column to normalize features
    means = {}
    stds = {}
    for i in num_indices:
        vals = [r[i] for r in rows if r[i] != '?']
        if not vals:
            continue
        means[i] = sum(vals) / len(vals)
        variance = sum((x - means[i]) ** 2 for x in vals) / len(vals)
        stds[i] = (variance ** 0.5) if variance > 0 else 1.0

    # Calculate anomaly score for each row
    # Score = Average absolute Z-score across all numeric features
    scores = []
    for idx, row in enumerate(rows):
        row_z_scores = []
        for i in num_indices:
            val = row[i]
            if val == '?':
                continue
            z = abs(val - means[i]) / stds[i]
            row_z_scores.append(z)
        
        if row_z_scores:
            avg_z = sum(row_z_scores) / len(row_z_scores)
            scores.append((idx, avg_z))
        else:
            scores.append((idx, 0))

    # Sort by score descending (most suspicious/outlier first)
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in scores]

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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspects = spot(header, rows)
    
    print("Outlier Detection Analysis:")
    print("The following rows represent employees who are statistically 'unlike' the current workforce.")
    print("Estimates for these individuals are less reliable due to their unique profiles.")
    print(f"Top 5 most unique/suspicious row indices: {suspects[:5]}")
    print("\nLogic: We calculate the average Z-score of numeric features for each row. "
          "Rows with high deviation from the population mean are flagged as outliers.")
