import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    A row is 'bad' if its goals are significantly worse than the median.
    We compare the distribution of input values in 'bad' rows vs 'good' rows.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]

    def get_row_score(row):
        # Normalize goals: lower MRE is better, higher ACC/PRED is better
        # We use a simple aggregate score relative to the dataset range
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

    # For each input, check if the mean/distribution differs significantly
    # We return columns where the 'bad' rows have a distinct average
    blamed = []
    for i in input_indices:
        if header[i] == 'criterion':
            # Symbolic: check if a specific criterion is over-represented in bad rows
            bad_vals = [r[i] for r in bad_rows]
            good_vals = [r[i] for r in good_rows]
            if bad_vals.count('squared_error') > good_vals.count('squared_error'):
                blamed.append(header[i])
        else:
            # Numeric: check if mean is significantly higher/lower
            bad_avg = sum(r[i] for r in bad_rows) / len(bad_rows)
            good_avg = sum(r[i] for r in good_rows) / len(good_rows)
            if abs(bad_avg - good_avg) / (good_avg + 1e-9) > 0.2:
                blamed.append(header[i])
                
    return blamed

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        culprits = blame(header, rows)
        print("The following settings are most responsible for poor performance:")
        for col in culprits:
            print(f"- {col}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
