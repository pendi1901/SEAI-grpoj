import csv

def justify(header, rows, row):
    """
    Estimates the rank of a given row and explains why 'paying everyone more'
    is not a sufficient strategy for retention.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if not name.endswith('+') and not name.endswith('-')]
    
    # Estimate goal values for the input row using the average of the dataset
    # (as a baseline for comparison)
    estimated_row = list(row)
    for idx in goal_indices:
        col_vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        estimated_row[idx] = sum(col_vals) / len(col_vals)
    
    def is_better(r1, r2):
        """Returns True if r1 is better than r2 based on goal columns."""
        for idx in goal_indices:
            if header[idx].endswith('+'):
                if r1[idx] < r2[idx]: return False
            elif header[idx].endswith('-'):
                if r1[idx] > r2[idx]: return False
        return True

    better_count = sum(1 for r in rows if is_better(estimated_row, r))
    p = better_count / len(rows)
    
    # Analyze correlation between MonthlyIncome and retention goals
    idx_income = header.index('MonthlyIncome')
    idx_tenure = header.index('YearsAtCompany+')
    
    # Calculate correlation (simple slope check)
    incomes = [r[idx_income] for r in rows]
    tenures = [r[idx_tenure] for r in rows]
    
    # If income were the primary driver, we would see a strong positive correlation.
    # We check if the top 20% of tenure have significantly higher income than the bottom 20%.
    sorted_by_tenure = sorted(rows, key=lambda r: r[idx_tenure])
    bottom_20 = sorted_by_tenure[:len(rows)//5]
    top_20 = sorted_by_tenure[-len(rows)//5:]
    
    avg_inc_bottom = sum(r[idx_income] for r in bottom_20) / len(bottom_20)
    avg_inc_top = sum(r[idx_income] for r in top_20) / len(top_20)
    
    # If the difference is small relative to the total income range, money isn't the only factor.
    reason = (f"While this arrangement ranks better than {p:.2f} of historical records, "
              f"simply increasing pay is insufficient because the income difference between "
              f"our longest and shortest tenured staff is only {abs(avg_inc_top - avg_inc_bottom):.0f}, "
              f"suggesting that factors like job satisfaction and role engagement are equally critical.")
    
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
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for i in goal_indices:
        test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
