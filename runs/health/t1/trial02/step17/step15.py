import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    A row is 'bad' if its goals are significantly worse than the median.
    We return the names of input columns that are most strongly associated
    with these 'bad' rows.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]

    def get_row_score(row):
        # Normalize goals: lower MRE is better, higher ACC/PRED is better
        score = 0
        for i in goal_indices:
            vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
            if not vals: continue
            min_v, max_v = min(vals), max(vals)
            norm = (row[i] - min_v) / (max_v - min_v) if max_v > min_v else 0
            if header[i].endswith('-'):
                score -= norm
            else:
                score += norm
        return score

    # Split into bad (bottom 25%) and good (top 25%)
    scored = sorted([(get_row_score(r), r) for r in rows], key=lambda x: x[0])
    n = len(scored) // 4
    bad_rows = [x[1] for x in scored[:n]]
    good_rows = [x[1] for x in scored[-n:]]

    # Identify columns where the distribution in 'bad' rows is significantly different
    # from 'good' rows. If a column is NOT in this list, it's a candidate for factory default.
    # The prompt asks for columns that explain why the worst rows are bad.
    culprits = []
    for i in input_indices:
        if header[i] == 'criterion':
            # Symbolic: check if a specific criterion is over-represented in bad rows
            bad_vals = [r[i] for r in bad_rows]
            good_vals = [r[i] for r in good_rows]
            if bad_vals.count('squared_error') > good_vals.count('squared_error'):
                culprits.append(header[i])
        else:
            # Numeric: check if mean is significantly higher/lower
            bad_avg = sum(r[i] for r in bad_rows) / len(bad_rows)
            good_avg = sum(r[i] for r in good_rows) / len(good_rows)
            # If the difference is small, it's not a culprit
            if abs(bad_avg - good_avg) / (good_avg + 1e-9) > 0.1:
                culprits.append(header[i])
                
    return culprits

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        culprits = blame(header, rows)
        input_cols = [name for name in header if not (name.endswith('-') or name.endswith('+'))]
        safe_defaults = [col for col in input_cols if col not in culprits]
        
        print("Settings you can safely leave at factory defaults:")
        for col in safe_defaults:
            print(f"- {col}")
        print("\nSettings that significantly impact performance (avoid changing blindly):")
        for col in culprits:
            print(f"- {col}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
