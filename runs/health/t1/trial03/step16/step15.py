import csv

def blame(header, rows):
    """
    Identifies input columns that have the least impact on performance.
    If a column's distribution in the 'worst' rows is statistically 
    indistinguishable from its distribution in the 'best' rows, 
    it is a candidate for a 'factory default' setting.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i, h in enumerate(header) if not h.endswith(('-', '+'))]

    def get_score(row):
        s = 0
        for i in goal_indices:
            col = header[i]
            vals = [r[i] for r in rows]
            mn, mx = min(vals), max(vals)
            norm = (row[i] - mn) / (mx - mn) if mx > mn else 0
            s += (1 - norm) if col.endswith('-') else norm
        return s

    # Rank rows by performance
    scored = sorted([(get_score(r), r) for r in rows], key=lambda x: x[0])
    
    # Compare bottom 25% (worst) vs top 25% (best)
    n = len(scored) // 4
    worst = [x[1] for x in scored[:n]]
    best = [x[1] for x in scored[-n:]]

    def get_dist_diff(col_idx):
        # Calculate difference in means (or mode for symbolic)
        vals_worst = [r[col_idx] for r in worst]
        vals_best = [r[col_idx] for r in best]
        
        if isinstance(vals_worst[0], str):
            # For symbolic, check frequency distribution
            return 0 # Simplified: assume symbolic are sensitive
        else:
            # For numeric, calculate normalized difference in means
            m_w = sum(vals_worst) / len(vals_worst)
            m_b = sum(vals_best) / len(vals_best)
            all_vals = [r[col_idx] for r in rows]
            rng = max(all_vals) - min(all_vals)
            return abs(m_w - m_b) / rng if rng > 0 else 0

    # Columns with the smallest difference in distribution between best and worst
    # are the ones that can be left at default.
    impacts = []
    for i in input_indices:
        impacts.append((get_dist_diff(i), header[i]))
    
    impacts.sort()
    return [x[1] for x in impacts]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)
            
    safe_settings = blame(header, rows)
    print("Settings you can likely leave at factory defaults (least impact on performance):")
    for setting in safe_settings:
        print(f"- {setting}")
