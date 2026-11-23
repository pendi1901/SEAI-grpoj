import csv

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' or contain 
    erroneous data. We use an anomaly detection approach:
    1. Calculate the mean and standard deviation for all numeric inputs.
    2. Flag rows that have extreme values (Z-score > 3) or logical 
       inconsistencies (e.g., tenure > age).
    """
    idx_map = {name: i for i, name in enumerate(header)}
    numeric_indices = [i for i, col in enumerate(header) if header[i][0].isupper() and not (col.endswith('+') or col.endswith('-'))]
    
    # Calculate stats for numeric inputs
    stats = {}
    for i in numeric_indices:
        vals = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if not vals: continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std if std > 0 else 1.0)

    suspects = []
    for i, row in enumerate(rows):
        score = 0
        
        # 1. Statistical Outlier Check (Z-score)
        for idx in numeric_indices:
            if idx in stats:
                mean, std = stats[idx]
                z = abs(row[idx] - mean) / std
                if z > 3:
                    score += z
        
        # 2. Logical Inconsistency Check
        # Age vs TotalWorkingYears
        if 'Age' in idx_map and 'TotalWorkingYears' in idx_map:
            if row[idx_map['Age']] < (row[idx_map['TotalWorkingYears']] + 16):
                score += 5
        
        # YearsInCurrentRole vs TotalWorkingYears
        if 'YearsInCurrentRole+' in idx_map and 'TotalWorkingYears' in idx_map:
            if row[idx_map['YearsInCurrentRole+']] > row[idx_map['TotalWorkingYears']]:
                score += 5

        if score > 0:
            suspects.append((score, i))

    # Sort by score descending
    suspects.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in suspects]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    suspects = spot(header, rows)
    
    print("Anomaly Detection: Identifying unreliable estimates.")
    print(f"We identified {len(suspects)} rows that are statistically or logically anomalous.")
    print("These rows represent profiles unlike our historical data, meaning our "
          "estimates for them are likely unreliable.")
    print(f"Top 5 most suspicious row indices: {suspects[:5]}")
