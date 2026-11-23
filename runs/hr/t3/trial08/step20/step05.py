import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with short stays (low YearsAtCompany+).
    We define 'worst rows' as those in the bottom 25% of 'YearsAtCompany+'.
    We then identify which input columns have the strongest correlation with 
    these low values.
    """
    years_idx = header.index('YearsAtCompany+')
    
    # Filter out goal columns
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('+') or name.endswith('-'))
    ]
    
    # Sort rows by YearsAtCompany+ ascending (lower is worse)
    sorted_rows = sorted(rows, key=lambda r: r[years_idx])
    
    # Define 'worst' as the bottom 25%
    limit = len(rows) // 4
    worst_rows = sorted_rows[:limit]
    
    # Calculate average for each input column in the worst group
    # and compare to the global average to find "drivers" of short stays
    scores = []
    for i in input_indices:
        col_data = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not col_data:
            continue
            
        global_avg = sum(col_data) / len(col_data)
        worst_avg = sum(r[i] for r in worst_rows if isinstance(r[i], (int, float))) / len(worst_rows)
        
        # We look for features where the worst group deviates significantly from the mean
        # For numeric, we look at the absolute difference
        diff = abs(worst_avg - global_avg)
        scores.append((diff, header[i]))
    
    # Sort by difference and return the top 3 column names
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for diff, name in scores[:3]]

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
    
    results = blame(header, rows)
    print("The input columns that best explain short stays are:")
    for col in results:
        print(f"- {col}")
    print("\nThese columns show the most significant deviation in the bottom 25% of tenure.")
