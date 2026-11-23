import csv

def spot(header, rows):
    """
    Identifies rows that contain input values that are likely entered wrongly.
    We define 'suspicious' as rows containing values that are extreme outliers
    (outside 3 standard deviations) for numeric columns, or rare categories
    for symbolic columns. Returns indices of rows, most suspicious first.
    """
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    symbolic_indices = [i for i, name in enumerate(header) if not name[0].isupper()]
    
    # Calculate stats for numeric columns
    num_stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if len(vals) > 1:
            mean = sum(vals) / len(vals)
            std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
            num_stats[i] = (mean, std)
            
    # Calculate frequencies for symbolic columns
    sym_stats = {}
    for i in symbolic_indices:
        vals = [r[i] for r in rows]
        total = len(vals)
        counts = {}
        for v in vals:
            counts[v] = counts.get(v, 0) + 1
        sym_stats[i] = {k: v / total for k, v in counts.items()}
        
    row_scores = []
    for idx, row in enumerate(rows):
        score = 0
        # Numeric outliers (Z-score > 3)
        for i in numeric_indices:
            if i in num_stats and isinstance(row[i], (int, float)):
                mean, std = num_stats[i]
                if std > 0:
                    z = abs(row[i] - mean) / std
                    if z > 3:
                        score += z
        
        # Rare symbolic values (frequency < 1%)
        for i in symbolic_indices:
            val = row[i]
            if val in sym_stats[i] and sym_stats[i][val] < 0.01:
                score += 5 # Penalty for rare category
                
        if score > 0:
            row_scores.append((idx, score))
            
    # Sort by score descending
    row_scores.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in row_scores]

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
            
    suspicious = spot(header, rows)
    
    print("Data Integrity Report: Suspicious Records")
    print("The following rows contain values that are statistically extreme or rare,")
    print("suggesting the data may be unreliable for these specific entries:")
    for idx in suspicious[:5]:
        print(f"- Row {idx}: Contains anomalous input values.")
    
    if not suspicious:
        print("No suspicious records detected.")
