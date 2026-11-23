import csv

def get_utility(header, row):
    """
    Calculates a normalized utility score for a row.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Normalize goals to [0, 1]
    mre = min(1.0, max(0.0, row[mre_idx]))
    acc = min(1.0, max(0.0, row[acc_idx]))
    pred = min(1.0, max(0.0, row[pred_idx]))
    
    return (1.0 - mre) + acc + pred

def blame(header, rows):
    """
    Identifies input columns that have the least impact on performance.
    If a column's distribution in the 'worst' rows is statistically similar 
    to the global distribution, it can be left at factory defaults.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate utility and sort to find the worst 20%
    scored_rows = sorted([(get_utility(header, r), r) for r in rows], key=lambda x: x[0])
    n_worst = max(1, len(rows) // 5)
    worst_rows = [r for _, r in scored_rows[:n_worst]]
    
    # For each input, calculate the difference in mean/distribution
    # between the worst rows and the global set.
    # Low impact means the setting doesn't correlate with being "bad".
    impacts = []
    for i in input_indices:
        col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not col_vals: continue
        
        global_mean = sum(col_vals) / len(col_vals)
        worst_vals = [r[i] for r in worst_rows if isinstance(r[i], (int, float))]
        if not worst_vals: continue
        
        worst_mean = sum(worst_vals) / len(worst_vals)
        
        # Impact is the normalized deviation
        std_dev = (sum((x - global_mean)**2 for x in col_vals) / len(col_vals))**0.5
        score = abs(worst_mean - global_mean) / (std_dev if std_dev > 0 else 1)
        impacts.append((score, header[i]))
    
    # Sort by impact ascending: lowest impact means safest to leave at default
    impacts.sort(key=lambda x: x[0])
    
    return [name for _, name in impacts]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    safe_settings = blame(header, rows)
    print("Settings you can safely leave at factory defaults (least impact on performance):")
    for setting in safe_settings:
        print(f"- {setting}")
