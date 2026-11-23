import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with short stays.
    'YearsAtCompany+' is the goal to maximize. We define 'worst' as the 
    bottom 25% of employees by tenure. We then look for input features 
    that are statistically different in this group compared to the rest.
    """
    idx_tenure = header.index('YearsAtCompany+')
    
    # Sort rows by tenure to find the "worst" (shortest stays)
    sorted_rows = sorted(rows, key=lambda r: r[idx_tenure])
    cutoff = len(rows) // 4
    worst = sorted_rows[:cutoff]
    rest = sorted_rows[cutoff:]
    
    # Identify input columns (exclude goals)
    input_cols = [i for i, name in enumerate(header) 
                  if not (name.endswith('+') or name.endswith('-'))]
    
    scores = []
    for i in input_cols:
        # Calculate mean difference between worst and rest
        if isinstance(worst[0][i], (int, float)):
            val_worst = sum(r[i] for r in worst) / len(worst)
            val_rest = sum(r[i] for r in rest) / len(rest)
            diff = abs(val_worst - val_rest)
            scores.append((diff, header[i]))
        else:
            # For symbolic, check if the distribution of the most common value differs
            vals_w = [r[i] for r in worst]
            vals_r = [r[i] for r in rest]
            mode_w = max(set(vals_w), key=vals_w.count)
            # Score based on how much more frequent the mode is in the worst group
            freq_w = vals_w.count(mode_w) / len(vals_w)
            freq_r = vals_r.count(mode_w) / len(vals_r)
            scores.append((abs(freq_w - freq_r), header[i]))
            
    # Return top 3 columns that explain the short stays
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores[:3]]

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    factors = blame(header, rows)
    print("Factors explaining short stays at the company:")
    for factor in factors:
        print(f"- {factor}")
