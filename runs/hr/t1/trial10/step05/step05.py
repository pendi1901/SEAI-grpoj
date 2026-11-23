import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with low 'YearsAtCompany+' 
    (the goal to maximize). We look for columns where the values in the 
    bottom 20% of tenure differ significantly from the rest.
    """
    yac_idx = header.index('YearsAtCompany+')
    
    # Identify input columns (exclude goals)
    input_indices = [
        i for i, name in enumerate(header)
        if not (name.endswith('+') or name.endswith('-'))
    ]
    
    # Sort rows by YearsAtCompany+ (ascending) to find the "worst" (shortest stay)
    sorted_rows = sorted(rows, key=lambda r: r[yac_idx])
    limit = max(1, len(rows) // 5)
    worst = sorted_rows[:limit]
    rest = sorted_rows[limit:]
    
    scores = []
    for i in input_indices:
        col_name = header[i]
        val_worst = [r[i] for r in worst]
        val_rest = [r[i] for r in rest]
        
        # Calculate a simple "difference" score
        # For numeric: difference in means
        # For symbolic: difference in frequency of the most common value
        if isinstance(val_worst[0], (int, float)):
            m1 = sum(val_worst) / len(val_worst)
            m2 = sum(val_rest) / len(val_rest)
            score = abs(m1 - m2)
        else:
            # Frequency of the most common value in 'worst'
            mode_w = max(set(val_worst), key=val_worst.count)
            freq_w = val_worst.count(mode_w) / len(val_worst)
            freq_r = val_rest.count(mode_w) / len(val_rest)
            score = abs(freq_w - freq_r)
            
        scores.append((score, col_name))
    
    # Return top 3 columns that explain the short stays
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores[:3]]

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
            
    results = blame(header, rows)
    print("Factors contributing to short employee tenure:")
    for factor in results:
        print(f"- {factor}")
    print("\nThese columns show the strongest correlation with employees who leave early.")
