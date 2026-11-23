import csv
import step05

def blame(header, rows):
    """
    Identifies input columns that have 'nothing to do' with how long people stay.
    We define these as columns that show the least difference between the 
    'worst' performers (bottom 20% by 'YearsAtCompany+') and the global average.
    """
    years_idx = header.index('YearsAtCompany+')
    
    # Filter out rows with valid numeric years
    valid_rows = [r for r in rows if isinstance(r[years_idx], (int, float))]
    valid_rows.sort(key=lambda x: x[years_idx])
    
    # Worst 20%
    worst = valid_rows[:max(1, len(valid_rows) // 5)]
    
    # Identify input columns (not goals)
    input_indices = [
        i for i, name in enumerate(header)
        if not (name.endswith('+') or name.endswith('-'))
    ]
    
    # Calculate global averages and worst-group averages
    # We look for features where the difference is minimal (i.e., they don't distinguish the worst)
    scores = []
    for i in input_indices:
        col_data = [r[i] for r in valid_rows if isinstance(r[i], (int, float))]
        if not col_data:
            continue
        
        global_avg = sum(col_data) / len(col_data)
        worst_avg = sum(r[i] for r in worst if isinstance(r[i], (int, float))) / len(worst)
        
        # Small difference means the feature is not a strong indicator of 'bad' performance
        diff = abs(global_avg - worst_avg)
        scores.append((diff, header[i]))
    
    # Return columns with the smallest differences (least impact)
    scores.sort(key=lambda x: x[0])
    return [s[1] for s in scores[:5]]

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
    
    useless_factors = blame(header, rows)
    print("Columns that have little impact on retention (candidates for removal):")
    for factor in useless_factors:
        print(f"- {factor}")
