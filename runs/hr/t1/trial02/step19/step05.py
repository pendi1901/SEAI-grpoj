import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with low tenure (YearsAtCompany+).
    We define 'worst rows' as those in the bottom 25% of tenure.
    We then identify input columns where the average value for these 'worst'
    rows deviates most significantly from the global average.
    """
    yac_idx = header.index('YearsAtCompany+')
    
    # Identify input columns (numeric or symbolic, excluding goals)
    input_indices = [i for i, name in enumerate(header) 
                     if not name.endswith('+') and not name.endswith('-')]
    
    # Sort rows by tenure to find the 'worst' (bottom 25%)
    sorted_rows = sorted(rows, key=lambda r: r[yac_idx])
    worst_rows = sorted_rows[:len(rows) // 4]
    
    # Calculate global averages/modes for inputs
    def get_avg(idx):
        col_data = [r[idx] for r in rows]
        if isinstance(col_data[0], float):
            return sum(col_data) / len(col_data)
        else:
            # For symbolic, return the most frequent
            return max(set(col_data), key=col_data.count)

    # Calculate deviation for each input column
    deviations = []
    for i in input_indices:
        worst_val = [r[i] for r in worst_rows]
        if isinstance(worst_val[0], float):
            avg_all = get_avg(i)
            avg_worst = sum(worst_val) / len(worst_val)
            # Score based on how much the worst group differs from the mean
            score = abs(avg_worst - avg_all)
        else:
            # For symbolic, score based on frequency difference
            mode_all = get_avg(i)
            mode_worst = max(set(worst_val), key=worst_val.count)
            score = 1.0 if mode_worst != mode_all else 0.0
        
        deviations.append((header[i], score))
    
    # Return top 3 columns that explain the short stays
    deviations.sort(key=lambda x: x[1], reverse=True)
    return [d[0] for d in deviations[:3]]

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
            
    top_factors = blame(header, rows)
    
    print("Analysis of short-tenure roles:")
    print("The primary factors associated with employees leaving early are:")
    for factor in top_factors:
        print(f"- {factor}")
    print("\nThese columns show the highest variance between the general population")
    print("and those with the shortest tenure at the company.")
