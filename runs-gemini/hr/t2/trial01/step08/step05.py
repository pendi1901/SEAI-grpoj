import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with short tenure (YearsAtCompany+).
    'Worst' rows are those with the lowest tenure.
    We compare the average of input columns in the bottom 20% of tenure
    against the rest of the population.
    """
    tenure_idx = header.index("YearsAtCompany+")
    
    # Sort rows by tenure to find the 'worst' (shortest stayers)
    sorted_rows = sorted(rows, key=lambda r: r[tenure_idx])
    cutoff = max(1, len(rows) // 5)
    worst = sorted_rows[:cutoff]
    rest = sorted_rows[cutoff:]
    
    # Identify input columns (exclude goals)
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('+') or h.endswith('-'))]
    
    differences = []
    for i in input_indices:
        col_name = header[i]
        # Only analyze numeric inputs for simple difference comparison
        if isinstance(worst[0][i], (int, float)):
            avg_worst = sum(r[i] for r in worst) / len(worst)
            avg_rest = sum(r[i] for r in rest) / len(rest)
            # We look for features where the 'worst' group has significantly lower values
            # than the rest, suggesting a potential cause for short stays.
            diff = avg_rest - avg_worst
            differences.append((diff, col_name))
            
    # Sort by the largest positive difference (where 'worst' are significantly lower)
    differences.sort(key=lambda x: x[0], reverse=True)
    
    return [d[1] for d in differences[:3]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
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
    print("Factors associated with short employee tenure:")
    for factor in results:
        print(f"- {factor}")
