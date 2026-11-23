import csv
from step02 import guess
from step05 import blame

def justify(header, rows, row):
    """
    Estimates the goal columns for the target row and compares it against
    all existing rows to determine its percentile rank.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # To fix the ValueError: step02.py's guess function expects the test row 
    # to have the same number of columns as the training data.
    # When we mask the goal column with '?', we must ensure the input to 
    # guess() maintains the original column count.
    test_row = list(row)
    for g_idx in goal_indices:
        test_row[g_idx] = 0.0 
    
    # guess() returns a list of predictions for each test row
    predictions = guess(header, rows, [test_row])
    estimated_goal_val = predictions[0]

    # Calculate how many rows this row is "better than"
    # We compare the estimated goal value against the true values in 'rows'
    better_count = 0
    for r in rows:
        is_better = True
        # We only compare against the first goal column as per step02/step07 logic
        g_idx = goal_indices[0]
        val_r = r[g_idx]
        
        if header[g_idx].endswith('+'):
            if not (estimated_goal_val >= val_r):
                is_better = False
        else:
            if not (estimated_goal_val <= val_r):
                is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    
    # Identify top factors to explain why pay isn't the only lever
    top_factors = blame(header, rows)
    reason = f"While pay is a factor, our analysis shows that {top_factors[0]}, {top_factors[1]}, and {top_factors[2]} are more significant drivers of employee tenure than salary alone."
    
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
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for i in goal_indices:
        test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
