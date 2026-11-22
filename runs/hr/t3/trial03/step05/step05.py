import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with short stays ('YearsAtCompany+').
    We define 'worst rows' as the bottom 20% of employees by tenure.
    We then compare the distribution of input features in these short-stay 
    employees against the rest of the population to find the most 
    discriminating factors.
    """
    goal_idx = header.index('YearsAtCompany+')
    
    # Sort rows by tenure to find the "worst" (shortest stay)
    sorted_rows = sorted(rows, key=lambda x: x[goal_idx])
    cutoff = max(1, len(rows) // 5)
    worst = sorted_rows[:cutoff]
    rest = sorted_rows[cutoff:]
    
    # Identify input columns (exclude goals)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('+') or name.endswith('-'))]
    
    scores = []
    for i in input_indices:
        col_name = header[i]
        # Calculate simple difference in means/proportions
        if isinstance(worst[0][i], float):
            w_val = sum(r[i] for r in worst) / len(worst)
            r_val = sum(r[i] for r in rest) / len(rest)
            diff = abs(w_val - r_val)
        else:
            # For symbolic, compare frequency of the most common value in 'worst'
            w_vals = [r[i] for r in worst]
            r_vals = [r[i] for r in rest]
            mode_w = max(set(w_vals), key=w_vals.count)
            diff = abs(w_vals.count(mode_w) / len(w_vals) - r_vals.count(mode_w) / len(r_vals))
        
        scores.append((diff, col_name))
    
    # Return top 3 columns that explain the difference
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in scores[:3]]

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
    print("Factors most associated with short employee tenure:")
    for f in factors:
        print(f"- {f}")
