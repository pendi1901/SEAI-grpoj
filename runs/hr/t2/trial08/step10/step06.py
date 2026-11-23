import csv
import step02

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the ranking.
    """
    # Identify goal columns
    goals = [(i, name) for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Estimate goal values for the input row using the average from the dataset
    # (Using step02 logic for estimation)
    estimates = {}
    for idx, name in goals:
        vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        estimates[idx] = sum(vals) / len(vals) if vals else 0.0
    
    # Define "better" logic:
    # For '+', higher is better. For '-', lower is better.
    def is_better(r1, r2):
        for idx, name in goals:
            v1 = r1[idx] if r1[idx] != "?" else estimates[idx]
            v2 = r2[idx]
            if name.endswith('+'):
                if v1 < v2: return False
            else:
                if v1 > v2: return False
        return True

    # Calculate fraction of rows that the input row is better than
    better_count = sum(1 for r in rows if is_better(estimates, r))
    p = better_count / len(rows)
    
    reason = f"This team arrangement ranks in the top {int((1-p)*100)}% of all records based on its projected performance across all goal metrics."
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Test with the first row as a sample
    test_row = rows[0][:]
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Ranking: {p:.4f}")
    print(f"Justification: {reason}")
