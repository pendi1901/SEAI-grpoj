import csv
import step03

def blame(header, rows):
    """
    Identifies input columns that have 'nothing to do' with how long people stay.
    We define 'nothing to do' as columns where the distribution of values 
    for the 'worst' employees (bottom 25% by tenure) is statistically 
    indistinguishable from the distribution of the 'best' employees 
    (top 25% by tenure).
    """
    # Identify goal column (first one ending in + or -)
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # Identify input columns
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('+') or name.endswith('-'))]
    
    # Sort rows by goal to find best and worst
    sorted_rows = sorted(rows, key=lambda r: r[goal_idx], reverse=is_maximize)
    n = len(rows)
    quarter = max(1, n // 4)
    worst = sorted_rows[:quarter]
    best = sorted_rows[-quarter:]
    
    useless_cols = []
    for i in input_indices:
        # Only analyze numeric columns for statistical similarity
        if isinstance(rows[0][i], (int, float)):
            worst_vals = [r[i] for r in worst]
            best_vals = [r[i] for r in best]
            
            # If the distributions are statistically similar (noise), 
            # the column likely has no impact on the goal.
            if step03.certify(worst_vals, best_vals):
                useless_cols.append(header[i])
                
    return useless_cols

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

    useless = blame(header, rows)
    print("Columns that appear to have no significant impact on employee tenure:")
    for col in useless:
        print(f"- {col}")
