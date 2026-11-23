import csv
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the goal columns for the target row and compares it against
    all existing rows to determine its percentile rank.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Estimate the missing goal values for the target row
    # We use the guess function from step02. 
    # To avoid the ValueError in step02's transform_row, we must ensure 
    # the test row passed to guess has the goal column filled with a dummy value 
    # that the encoder can handle, or handle the '?' inside the logic.
    # Since step02 expects '?' to be handled, we provide a dummy numeric value 
    # for the goal column so the encoder doesn't crash.
    
    estimated_goals = {}
    for g_idx in goal_indices:
        test_row = list(row)
        # Provide a dummy float value for the goal column so step02's transform_row succeeds
        test_row[g_idx] = 0.0 
        
        pred = guess(header, rows, [test_row])
        estimated_goals[g_idx] = pred[0]

    # Calculate how many rows this row is "better than"
    better_count = 0
    for r in rows:
        is_better = True
        for g_idx in goal_indices:
            val_r = r[g_idx]
            val_target = estimated_goals[g_idx]
            
            if header[g_idx].endswith('+'):
                if not (val_target >= val_r):
                    is_better = False
            else:
                if not (val_target <= val_r):
                    is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This employee's projected tenure metrics outperform {p:.1%} of the existing workforce."
    return p, reason

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
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
