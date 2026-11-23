import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with low 'YearsAtCompany+' (the goal).
    We define 'worst' as the bottom 20% of tenure.
    We return columns that have the highest difference in mean/distribution 
    between the worst performers and the rest.
    """
    tenure_idx = header.index('YearsAtCompany+')
    
    # Sort rows by tenure to find the bottom 20%
    sorted_rows = sorted(rows, key=lambda r: r[tenure_idx])
    limit = len(rows) // 5
    worst = sorted_rows[:limit]
    others = sorted_rows[limit:]
    
    # Identify input columns (not goals)
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('+') or name.endswith('-'))
    ]
    
    scores = []
    for i in input_indices:
        col_name = header[i]
        w_vals = [r[i] for r in worst if isinstance(r[i], (int, float))]
        o_vals = [r[i] for r in others if isinstance(r[i], (int, float))]
        
        if not w_vals or not o_vals:
            continue
            
        # Simple correlation: difference in means
        diff = abs((sum(w_vals) / len(w_vals)) - (sum(o_vals) / len(o_vals)))
        scores.append((diff, col_name))
    
    # Return top 3 columns that differentiate the worst performers
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    results = blame(header, rows)
    print("Factors explaining short stays (low YearsAtCompany+):")
    for factor in results:
        print(f"- {factor}")
