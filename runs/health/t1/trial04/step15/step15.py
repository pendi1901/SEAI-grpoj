import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with 'bad' performance.
    A row is 'bad' if its aggregate goal score is in the bottom 20%.
    The columns that have the least impact on performance are the ones
    the customer can safely leave at factory defaults.
    """
    goal_indices = [i for i, name in enumerate(header) if '-' in name or '+' in name]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    
    # Normalize goals to calculate a single performance score
    # MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
    col_data = [[r[i] for r in rows] for i in range(len(header))]
    mins = [min(c) for c in col_data]
    maxs = [max(c) for c in col_data]
    
    def get_score(r):
        s = 0
        for i in goal_indices:
            rng = maxs[i] - mins[i]
            norm = (r[i] - mins[i]) / rng if rng > 0 else 0
            if header[i].endswith('-'):
                s += (1 - norm)
            else:
                s += norm
        return s

    # Rank rows by score
    scored_rows = sorted(rows, key=get_score)
    n = len(scored_rows)
    bad = scored_rows[:n // 5]
    good = scored_rows[n // 5:]
    
    # Calculate impact: difference in distribution between bad and good
    impacts = []
    for i in input_indices:
        col_name = header[i]
        if isinstance(rows[0][i], (int, float)):
            bad_vals = [r[i] for r in bad]
            good_vals = [r[i] for r in good]
            diff = abs((sum(bad_vals)/len(bad_vals)) - (sum(good_vals)/len(good_vals)))
            impacts.append((diff, col_name))
        else:
            cats = set(r[i] for r in rows)
            bad_dist = {c: sum(1 for r in bad if r[i] == c) / len(bad) for c in cats}
            good_dist = {c: sum(1 for r in good if r[i] == c) / len(good) for c in cats}
            diff = sum(abs(bad_dist[c] - good_dist[c]) for c in cats) / 2
            impacts.append((diff, col_name))
            
    # Sort by impact ascending: low impact means it's safe to leave at default
    impacts.sort(key=lambda x: x[0])
    return [x[1] for x in impacts]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    safe_settings = blame(header, rows)
    print("Settings you can safely leave at factory defaults (least impact on performance):")
    for name in safe_settings:
        print(f"- {name}")
