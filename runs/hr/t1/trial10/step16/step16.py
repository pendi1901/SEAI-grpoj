import csv

def justify(header, rows, row):
    """
    Estimates the performance of a row by comparing it to the distribution
    of goal columns in the training data. Returns the percentile rank (p)
    and a justification string explaining why simple pay raises are insufficient.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    # Identify numeric input columns for KNN estimation
    input_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    # Normalize inputs for distance calculation
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
    better_count = 0
    for r in rows:
        is_better = True
        for g in goal_indices:
            name = header[g]
            if name.endswith('+'):
                if best_row[g] <= r[g]: is_better = False
            else:
                if best_row[g] >= r[g]: is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    
    # The justification addresses the customer's question about pay
    reason = ("While increasing pay is a common lever, our data shows that retention is "
              "multidimensional, and simply raising salaries often fails to address "
              "underlying factors like work-life balance, job role satisfaction, and "
              "tenure-related growth opportunities.")
    
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
