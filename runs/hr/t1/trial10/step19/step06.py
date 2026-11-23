import csv

def justify(header, rows, row):
    """
    Estimates the performance of a row by comparing it to the distribution
    of goal columns in the training data. Returns the percentile rank (p)
    and a justification string.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Identify numeric input columns for KNN estimation
    input_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    # Simple KNN to estimate goal values for the test row
    # Normalize inputs
    mins = [min(r[i] for r in rows) for i in input_indices]
    maxs = [max(r[i] for r in rows) for i in input_indices]
    ranges = [maxs[i] - mins[i] if maxs[i] != mins[i] else 1.0 for i in range(len(input_indices))]
    
    def get_dist(r1, r2):
        d = 0
        for idx, i in enumerate(input_indices):
            d += ((r1[i] - r2[i]) / ranges[idx]) ** 2
        return d**0.5

    # Find nearest neighbor to estimate goals
    best_row = min(rows, key=lambda r: get_dist(r, row))
    
    # Calculate how many rows this row is 'better than'
    # A row is better if its goals are closer to the ideal (max for +, min for -)
    better_count = 0
    for r in rows:
        is_better = True
        for g in goal_indices:
            name = header[g]
            val_row = best_row[g]
            val_r = r[g]
            if name.endswith('+'):
                if val_row <= val_r:
                    is_better = False
            else: # ends with -
                if val_row >= val_r:
                    is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all teams because its projected retention metrics outperform {int(p*100)}% of historical records."
    
    return p, reason

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
            
    # Test with the first row, masking its goal columns
    test_row = rows[0][:]
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for g in goal_indices:
        test_row[g] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Percentile Rank: {p:.4f}")
    print(f"Justification: {reason}")
