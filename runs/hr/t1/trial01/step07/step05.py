import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with low tenure (YearsAtCompany+).
    We define 'worst rows' as those in the bottom 20% of tenure.
    We then identify which input columns have the highest variance or 
    distinctive values in these low-tenure rows compared to the rest.
    """
    tenure_idx = header.index('YearsAtCompany+')
    
    # Filter out goal columns and identify input columns
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('+') or name.endswith('-'))
    ]
    
    # Sort rows by tenure to find the 'worst' (lowest tenure)
    sorted_rows = sorted(rows, key=lambda r: r[tenure_idx])
    worst_rows = sorted_rows[:int(len(rows) * 0.2)]
    
    # For each input column, calculate how much the values in 'worst' rows
    # differ from the global average/distribution.
    # We look for columns where the values are most concentrated or distinct.
    scores = []
    for i in input_indices:
        col_name = header[i]
        values = [r[i] for r in worst_rows]
        
        # Simple heuristic: if numeric, check if the mean is significantly lower/higher
        # than the global mean. If symbolic, check for high frequency of a specific value.
        if isinstance(values[0], float):
            global_mean = sum(r[i] for r in rows) / len(rows)
            worst_mean = sum(values) / len(values)
            diff = abs(global_mean - worst_mean)
            scores.append((diff, col_name))
        else:
            # For symbolic, check if one value dominates the worst rows
            counts = {}
            for v in values:
                counts[v] = counts.get(v, 0) + 1
            max_freq = max(counts.values()) / len(values)
            scores.append((max_freq, col_name))
            
    # Return the top 3 columns that best explain the short stays
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
            
    factors = blame(header, rows)
    
    print("Analysis: Factors contributing to short employee tenure:")
    for factor in factors:
        print(f"- {factor}")
    print("\nThese columns show the strongest correlation with employees who leave early.")
