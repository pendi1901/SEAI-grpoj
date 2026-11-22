import csv

def spot(header, rows):
    """
    Identifies rows that are 'outliers' in the input space.
    Rows with input values that are statistically far from the mean 
    of their respective columns are flagged as potentially failed runs.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate means and standard deviations for numeric inputs
    stats = {}
    for i in input_indices:
        col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if col_vals:
            mean = sum(col_vals) / len(col_vals)
            var = sum((x - mean) ** 2 for x in col_vals) / len(col_vals)
            stats[i] = (mean, var ** 0.5)

    # Score rows based on Z-score of their inputs
    # Higher Z-score = more suspicious
    suspicion = []
    for row_idx, row in enumerate(rows):
        z_scores = []
        for i in input_indices:
            val = row[i]
            if i in stats:
                mean, std = stats[i]
                if std > 0:
                    z_scores.append(abs(val - mean) / std)
        
        if z_scores:
            # Use the maximum Z-score found in the row as the suspicion level
            suspicion.append((max(z_scores), row_idx))
    
    # Sort by suspicion descending
    suspicion.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in suspicion[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print(f"Analysis complete. Identified {len(suspicious_indices)} potentially failed runs.")
        print("Most suspicious row indices:", suspicious_indices[:10])
        print("These rows contain input values that deviate significantly from the norm.")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
