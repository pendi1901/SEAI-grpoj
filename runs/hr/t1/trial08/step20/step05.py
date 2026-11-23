import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with short stays ('YearsAtCompany+').
    We define 'worst rows' as the bottom 20% of employees by tenure.
    We then compare the average of input features in these 'worst' rows 
    against the global average to see which features deviate most.
    """
    # Identify goal and input columns
    years_idx = header.index('YearsAtCompany+')
    input_indices = [
        i for i, col in enumerate(header) 
        if not (col.endswith('+') or col.endswith('-'))
    ]
    
    # Sort rows by tenure to find the bottom 20%
    sorted_rows = sorted(rows, key=lambda r: r[years_idx])
    limit = max(1, int(len(rows) * 0.2))
    worst_rows = sorted_rows[:limit]
    
    # Calculate global averages for numeric inputs and modes for symbolic
    def get_stats(data_rows):
        stats = {}
        for i in input_indices:
            col_data = [r[i] for r in data_rows]
            if isinstance(col_data[0], (int, float)):
                stats[i] = sum(col_data) / len(col_data)
            else:
                # Mode for symbolic
                stats[i] = max(set(col_data), key=col_data.count)
        return stats

    global_stats = get_stats(rows)
    worst_stats = get_stats(worst_rows)
    
    # Identify features that differ most (for numeric) or differ at all (for symbolic)
    # We look for features where the 'worst' group deviates from the norm
    diffs = []
    for i in input_indices:
        col_name = header[i]
        if isinstance(global_stats[i], (int, float)):
            # Normalize difference
            val_diff = abs(worst_stats[i] - global_stats[i])
            diffs.append((val_diff, col_name))
        else:
            # Symbolic: if the mode is different, it's a strong indicator
            if worst_stats[i] != global_stats[i]:
                diffs.append((1.0, col_name))
    
    # Return top 3 columns that explain the short stays
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in diffs[:3]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = None
    
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
            
    factors = blame(header, rows)
    print("Analysis of short-stay employees:")
    print("The primary factors contributing to short tenure are:")
    for f in factors:
        print(f"- {f}")
    print("\nThese columns show the most significant deviation in employees who leave early.")
