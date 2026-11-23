import csv

def justify(header, rows, row):
    """
    Estimates the rank of a given row by comparing its goal performance 
    against all other rows in the dataset.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Simple estimation for goal columns: use the average of the dataset
    # (as a baseline since we don't have a complex model here)
    estimated_row = list(row)
    for idx in goal_indices:
        col_vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        estimated_row[idx] = sum(col_vals) / len(col_vals)
    
    def is_better(r1, r2):
        """Returns True if r1 is better than r2."""
        for idx in goal_indices:
            name = header[idx]
            if name.endswith('+'):
                if r1[idx] < r2[idx]: return False
            elif name.endswith('-'):
                if r1[idx] > r2[idx]: return False
        return True

    better_count = sum(1 for r in rows if is_better(estimated_row, r))
    p = better_count / len(rows)
    
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of teams because it outperforms {int(p*100)}% of the historical records in retention-focused metrics."
    
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Test with the first row, masking its goals
    test_row = list(rows[0])
    for i in range(len(test_row)):
        if header[i].endswith('+') or header[i].endswith('-'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
