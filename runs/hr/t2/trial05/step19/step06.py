import csv
import step02

def justify(header, rows, row):
    """
    Estimates the goal performance of a row and returns its percentile rank
    relative to the provided dataset.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Estimate the goal values for the input row using k-NN
    # We reuse the logic from step02, but since step02.guess returns a list,
    # we adapt it for a single row.
    estimated_goals = []
    for g_idx in goal_indices:
        # Simple k-NN estimation for the specific goal
        # Use numeric inputs to find neighbors
        input_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
        
        distances = []
        for r in rows:
            dist = 0
            for i in input_indices:
                if isinstance(row[i], (int, float)) and isinstance(r[i], (int, float)):
                    dist += (row[i] - r[i]) ** 2
            distances.append((dist**0.5, r[g_idx]))
        
        distances.sort(key=lambda x: x[0])
        k = 5
        avg_val = sum(n[1] for n in distances[:k]) / k
        estimated_goals.append((g_idx, avg_val))
    
    # Calculate percentile rank (fraction of rows the input row is better than)
    # A row is better if its goals are closer to the "best" (max for +, min for -)
    better_count = 0
    for r in rows:
        is_better = True
        for g_idx, est_val in estimated_goals:
            actual = r[g_idx]
            if header[g_idx].endswith('+'):
                if not (est_val >= actual):
                    is_better = False
            else: # ends with -
                if not (est_val <= actual):
                    is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This team arrangement ranks in the top {int((1-p)*100)}% of all records based on its projected retention metrics."
    
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
    
    # Test with the first row, masking its goal columns
    test_row = list(rows[0])
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
