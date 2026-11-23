import csv

def blame(header, rows):
    """
    Identifies which input columns have the least impact on performance.
    'Bad' rows are defined as the bottom 10% based on a multi-objective score.
    Settings that can be left at factory defaults are those whose distribution
    in 'bad' rows is statistically indistinguishable from their distribution
    in the 'good' rows (or the whole population).
    """
    # Identify goal indices
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')
    
    # Identify input indices
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Calculate a score for each row to define 'badness'
    # Normalize goals: MRE (min), ACC (max), PRED (max)
    def get_score(row):
        mre = row[idx_mre]
        acc = row[idx_acc]
        pred = row[idx_pred]
        # Simple relative score
        return -mre + acc + pred

    scored_rows = sorted([(get_score(r), r) for r in rows])
    
    # Define 'bad' as the bottom 10%
    n_bad = max(1, len(rows) // 10)
    bad_rows = [r for s, r in scored_rows[:n_bad]]
    
    # For each input, calculate the difference in mean/distribution between bad and all
    # If the difference is small, the setting is likely neutral (safe to default)
    neutral_settings = []
    for i in input_indices:
        col_name = header[i]
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        bad_vals = [r[i] for r in bad_rows if isinstance(r[i], (int, float))]
        
        if not vals or not bad_vals:
            continue
            
        mean_all = sum(vals) / len(vals)
        mean_bad = sum(bad_vals) / len(bad_vals)
        
        # Normalize difference by range
        range_v = max(vals) - min(vals) + 1e-9
        diff = abs(mean_bad - mean_all) / range_v
        
        # If the normalized difference is very low, it's a candidate for "safe to default"
        if diff < 0.05:
            neutral_settings.append(col_name)
            
    return neutral_settings

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] == 'criterion':
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        safe_settings = blame(header, rows)
        print("Settings that can be left at factory defaults without significant impact:")
        if safe_settings:
            for s in safe_settings:
                print(f"- {s}")
        else:
            print("None identified; all settings appear to influence performance.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
