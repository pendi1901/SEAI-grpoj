import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with short stays (low YearsAtCompany+).
    We define 'worst rows' as the bottom 25% of employees by tenure.
    We then compare the average of inputs in the 'worst' group vs the 'best' group.
    The columns with the largest normalized differences are returned as the 'blame'.
    """
    tenure_idx = header.index("YearsAtCompany+")
    
    # Filter out rows with missing goal data
    valid_rows = [r for r in rows if isinstance(r[tenure_idx], (int, float))]
    valid_rows.sort(key=lambda x: x[tenure_idx])
    
    # Split into bottom 25% (short stay) and top 25% (long stay)
    n = len(valid_rows) // 4
    worst = valid_rows[:n]
    best = valid_rows[-n:]
    
    # Identify input columns (not goals)
    input_indices = [
        i for i, h in enumerate(header) 
        if not (h.endswith('+') or h.endswith('-'))
    ]
    
    scores = []
    for i in input_indices:
        # Only analyze numeric inputs for correlation
        if isinstance(worst[0][i], (int, float)):
            w_vals = [r[i] for r in worst]
            b_vals = [r[i] for r in best]
            
            w_avg = sum(w_vals) / len(w_vals)
            b_avg = sum(b_vals) / len(b_vals)
            
            # Calculate absolute difference normalized by range
            all_vals = [r[i] for r in valid_rows]
            rng = max(all_vals) - min(all_vals)
            if rng > 0:
                diff = abs(w_avg - b_avg) / rng
                scores.append((diff, header[i]))
    
    # Return top 3 columns that explain the difference
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores[:3]]

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

    factors = blame(header, rows)
    
    print("Analysis: What factors contribute to short employee tenure?")
    print("The following input columns show the most significant differences between")
    print("the shortest-tenured employees and the longest-tenured employees:")
    for f in factors:
        print(f"- {f}")
    print("\nThese factors are the primary indicators associated with high turnover.")
