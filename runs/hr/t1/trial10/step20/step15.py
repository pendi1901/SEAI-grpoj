import csv

def blame(header, rows):
    """
    Identifies input columns that have the least correlation with the goal 
    'YearsAtCompany+' (the goal to maximize). We calculate the correlation 
    between each input and the goal, then return the columns with the 
    lowest correlation scores, suggesting they are candidates to stop collecting.
    """
    yac_idx = header.index('YearsAtCompany+')
    
    # Identify input columns (exclude goals)
    input_indices = [
        i for i, name in enumerate(header)
        if not (name.endswith('+') or name.endswith('-'))
    ]
    
    # Calculate correlation/importance for each input
    # We use a simple variance-based approach: how much does the input 
    # distinguish between high-tenure and low-tenure employees?
    
    # Sort by YearsAtCompany+
    sorted_rows = sorted(rows, key=lambda r: r[yac_idx])
    
    # Compare top 20% (long stay) vs bottom 20% (short stay)
    limit = max(1, len(rows) // 5)
    long_stay = sorted_rows[-limit:]
    short_stay = sorted_rows[:limit]
    
    scores = []
    for i in input_indices:
        col_name = header[i]
        val_long = [r[i] for r in long_stay]
        val_short = [r[i] for r in short_stay]
        
        # Calculate a "distinction" score
        if isinstance(val_long[0], (int, float)):
            # For numeric: difference in means normalized by range
            m1 = sum(val_long) / len(val_long)
            m2 = sum(val_short) / len(val_short)
            # Use absolute difference as a proxy for correlation
            score = abs(m1 - m2)
        else:
            # For symbolic: difference in distribution (Jensen-Shannon-like)
            unique_vals = set(val_long + val_short)
            score = 0
            for v in unique_vals:
                p1 = val_long.count(v) / len(val_long)
                p2 = val_short.count(v) / len(val_short)
                score += abs(p1 - p2)
            
        scores.append((score, col_name))
    
    # Sort by score ascending (lowest score = least impact/correlation)
    scores.sort(key=lambda x: x[0])
    
    # Return the names of the 5 columns with the lowest impact
    return [s[1] for s in scores[:5]]

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
    print("Columns with the least impact on employee retention (candidates to stop collecting):")
    for factor in results:
        print(f"- {factor}")
    print("\nThese columns show the weakest correlation with tenure and may be redundant.")
