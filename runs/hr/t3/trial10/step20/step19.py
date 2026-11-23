import csv

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' by detecting
    outliers in the input space. We use a Z-score approach on numeric inputs
    to find rows that are statistically distant from the population mean.
    
    Returns a list of row indices, sorted by the magnitude of their 
    deviation (most suspicious first).
    """
    # Identify numeric input columns (exclude goals)
    input_indices = [
        i for i, h in enumerate(header) 
        if h[0].isupper() and not (h.endswith('+') or h.endswith('-'))
    ]
    
    # Calculate means and standard deviations for numeric inputs
    stats = {}
    for i in input_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std if std > 0 else 1.0)
        
    # Calculate suspicion score for each row
    # The score is the average absolute Z-score across all numeric inputs
    suspicion = []
    for idx, row in enumerate(rows):
        z_scores = []
        for i in input_indices:
            if i in stats and isinstance(row[i], (int, float)):
                mean, std = stats[i]
                z_scores.append(abs((row[i] - mean) / std))
        
        if z_scores:
            avg_z = sum(z_scores) / len(z_scores)
            # Only flag as suspicious if they are significant outliers (e.g., > 3 std)
            if avg_z > 3.0:
                suspicion.append((avg_z, idx))
                
    # Sort by suspicion score descending
    suspicion.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion]

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
            
    suspect_indices = spot(header, rows)
    
    print("Outlier Detection: Employees unlike anyone we have employed")
    print(f"Total rows checked: {len(rows)}")
    print(f"Number of suspicious rows identified: {len(suspect_indices)}")
    print("\nTop 5 most suspicious rows (High deviation from population norms):")
    for idx in suspect_indices[:5]:
        print(f"Row {idx} is statistically distant from historical employee profiles.")
    
    print("\nNote: Estimates for these employees cannot be trusted as they fall outside")
    print("the range of our historical data.")
