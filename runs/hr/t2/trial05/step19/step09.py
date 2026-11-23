import csv

def spot(header, rows):
    """
    Identifies rows that look wrong by checking for outliers in numeric columns.
    A row is considered suspicious if any of its numeric values are more than 
    3 standard deviations away from the column mean.
    """
    suspicious = {}
    
    # Identify numeric columns
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    for idx in numeric_indices:
        col_vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if not col_vals:
            continue
            
        mean = sum(col_vals) / len(col_vals)
        variance = sum((x - mean) ** 2 for x in col_vals) / len(col_vals)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            continue
            
        # Flag rows where this column is an extreme outlier
        for i, row in enumerate(rows):
            val = row[idx]
            if isinstance(val, (int, float)):
                z_score = abs(val - mean) / std_dev
                if z_score > 3:
                    suspicious[i] = suspicious.get(i, 0) + z_score
                    
    # Sort by suspicion score descending
    sorted_indices = sorted(suspicious.keys(), key=lambda x: suspicious[x], reverse=True)
    return sorted_indices

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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    indices = spot(header, rows)
    
    print("Suspicious rows identified (potential data entry errors):")
    for i in indices[:10]:  # Print top 10 most suspicious
        print(f"Row {i} is highly suspicious due to extreme numeric values.")
