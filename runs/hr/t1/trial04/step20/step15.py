import csv

def blame(header, rows):
    """
    Identifies input columns that have the least correlation with the goal columns.
    We define 'useless' columns as those whose values show no significant 
    difference between the top 25% performers and the bottom 25% performers.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('+') or h.endswith('-'))]

    # Calculate a composite score for each row to rank performance
    # Goal +: higher is better, Goal -: lower is better
    def get_row_score(row):
        score = 0.0
        for g_idx in goal_indices:
            val = row[g_idx]
            if not isinstance(val, (int, float)):
                continue
            # Simple normalization relative to column range
            col_vals = [r[g_idx] for r in rows if isinstance(r[g_idx], (int, float))]
            min_v, max_v = min(col_vals), max(col_vals)
            norm = (val - min_v) / (max_v - min_v + 1e-9)
            if header[g_idx].endswith('-'):
                score += (1.0 - norm)
            else:
                score += norm
        return score

    # Rank rows and pick top/bottom quartiles
    scored_rows = sorted([(get_row_score(r), r) for r in rows], key=lambda x: x[0])
    n = len(scored_rows) // 4
    bottom_25 = [r[1] for r in scored_rows[:n]]
    top_25 = [r[1] for r in scored_rows[-n:]]

    # Find columns where the distribution is statistically similar between top and bottom
    useless_cols = []
    for i in input_indices:
        vals_bottom = [r[i] for r in bottom_25 if isinstance(r[i], (int, float))]
        vals_top = [r[i] for r in top_25 if isinstance(r[i], (int, float))]
        
        if not vals_bottom or not vals_top:
            continue
            
        m1, m2 = sum(vals_bottom)/len(vals_bottom), sum(vals_top)/len(vals_top)
        # If the means are very close, the column is likely irrelevant
        if abs(m1 - m2) < 0.05 * (max(vals_top + vals_bottom) - min(vals_top + vals_bottom) + 1e-9):
            useless_cols.append(header[i])

    return useless_cols

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

    useless = blame(header, rows)
    
    print("Analysis: Columns that appear to have little impact on retention goals:")
    for col in useless[:10]: # Print top 10
        print(f"- {col}")
    print("\nThese columns show negligible difference between high and low performing staff.")
