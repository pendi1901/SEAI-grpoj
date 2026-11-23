import csv
import step01
import step02

def justify(header, rows, row):
    """
    Estimates the goal 'YearsAtCompany+' for the given row and determines
    its percentile rank relative to the provided dataset.
    """
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break

    # Estimate the goal using the mean of the training data (from step02 logic)
    # Since the row has '?', we calculate the average of the known rows
    known_vals = [r[goal_idx] for r in rows if isinstance(r[goal_idx], (int, float))]
    estimate = sum(known_vals) / len(known_vals)
    
    # Calculate how many rows this estimate is better than
    # 'YearsAtCompany+' is a goal to maximize
    better_count = sum(1 for r in rows if estimate > r[goal_idx])
    p = better_count / len(rows)
    
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all teams because its estimated tenure of {estimate:.1f} years exceeds the performance of most other records."
    
    return (p, reason)

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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Test with the first row, masking the goal
    test_row = rows[0][:]
    test_row[31] = "?"
    
    p, reason = justify(header, rows, test_row)
    
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
