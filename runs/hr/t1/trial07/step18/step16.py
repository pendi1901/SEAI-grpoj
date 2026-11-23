import csv

def justify(header, rows, row):
    """
    Estimates the rank of a given row by comparing its predicted goals
    against the actual goals of the provided training rows.
    To answer the customer's question about paying everyone more, we analyze
    the correlation between 'MonthlyIncome' and the goal 'YearsAtCompany+'.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    input_indices = [i for i, h in enumerate(header) if i not in goal_indices]
    
    # Simple KNN-based estimation for the goal
    def get_dist(r1, r2):
        d = 0.0
        for i in input_indices:
            if isinstance(r1[i], (int, float)) and isinstance(r2[i], (int, float)):
                # Normalize numeric distance
                all_vals = [r[i] for r in rows]
                rng = max(all_vals) - min(all_vals)
                d += ((r1[i] - r2[i]) / (rng if rng != 0 else 1.0))**2
            else:
                d += 1.0 if r1[i] != r2[i] else 0.0
        return d**0.5

    # Estimate goal values for the input row
    predictions = {}
    for g_idx in goal_indices:
        # Find nearest neighbor
        best_dist = float('inf')
        best_val = 0.0
        for r in rows:
            dist = get_dist(row, r)
            if dist < best_dist:
                best_dist = dist
                best_val = r[g_idx]
        predictions[g_idx] = float(best_val)

    # Calculate how many rows this row is "better than"
    better_count = 0
    for r in rows:
        is_better = True
        for g_idx in goal_indices:
            val_row = predictions[g_idx]
            val_r = r[g_idx]
            if header[g_idx].endswith('+'):
                if not (val_row >= val_r):
                    is_better = False
            else:
                if not (val_row <= val_r):
                    is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    
    # Analyze correlation between MonthlyIncome and YearsAtCompany+
    inc_idx = header.index('MonthlyIncome')
    tenure_idx = header.index('YearsAtCompany+')
    incomes = [r[inc_idx] for r in rows]
    tenures = [r[tenure_idx] for r in rows]
    
    # Simple correlation check
    avg_inc = sum(incomes) / len(incomes)
    high_inc_tenure = sum(r[tenure_idx] for r in rows if r[inc_idx] > avg_inc) / len([r for r in rows if r[inc_idx] > avg_inc])
    low_inc_tenure = sum(r[tenure_idx] for r in rows if r[inc_idx] <= avg_inc) / len([r for r in rows if r[inc_idx] <= avg_inc])
    
    reason = f"While higher pay is beneficial, data shows that employees with above-average income stay an average of {high_inc_tenure:.1f} years compared to {low_inc_tenure:.1f} years for others, suggesting that pay alone is not the sole driver of retention."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
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

    # Test with the first row, masking its goals
    test_row = list(rows[0])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for g_idx in goal_indices:
        test_row[g_idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
