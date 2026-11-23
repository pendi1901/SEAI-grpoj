import csv

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with poor performance.
    'Bad' rows are defined as those in the bottom 25% of a normalized 
    multi-objective score. Columns that show little variance or have 
    negligible impact on the 'badness' are candidates for factory defaults.
    """
    goals = []
    inputs = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))
        elif name.endswith('+'):
            goals.append((i, 1))
        else:
            inputs.append(i)

    # Calculate a normalized score for each row
    scores = []
    for row in rows:
        score = 0
        for idx, direction in goals:
            # Simple linear normalization heuristic
            score += row[idx] if direction == 1 else -row[idx]
        scores.append(score)

    # Identify the worst 25% of rows
    sorted_scores = sorted(scores)
    threshold = sorted_scores[len(scores) // 4]
    bad_rows = [rows[i] for i, s in enumerate(scores) if s <= threshold]
    
    # Calculate average value of inputs for bad rows vs all rows
    # The 'blame' is the absolute difference in means.
    # Columns with low blame are safe to leave at factory defaults.
    impacts = []
    for i in inputs:
        col_data = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if not col_data:
            continue
        
        bad_col_data = [row[i] for row in bad_rows if isinstance(row[i], (int, float))]
        if not bad_col_data:
            continue
            
        avg_all = sum(col_data) / len(col_data)
        avg_bad = sum(bad_col_data) / len(bad_col_data)
        
        # Normalize the impact by the range of the column to make it comparable
        col_range = max(col_data) - min(col_data) + 1e-9
        impact = abs(avg_bad - avg_all) / col_range
        impacts.append((impact, header[i]))

    # Return the names of the input columns that contribute most to the 'badness'
    impacts.sort(key=lambda x: x[0], reverse=True)
    return [name for impact, name in impacts]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
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

    culprits = blame(header, rows)
    
    # The columns at the end of the list have the least impact on performance
    # and are the safest to leave at factory defaults.
    safe_defaults = culprits[-2:]
    
    print("Settings you can safely leave at factory defaults:")
    for s in safe_defaults:
        print(f"- {s}")
    
    exit(0)
