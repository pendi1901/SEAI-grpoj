import csv
import step02

def justify(header, rows, row):
    """
    Estimates the performance of a row and returns its percentile rank 
    relative to the provided dataset.
    """
    # Identify goal columns
    goals = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    # Estimate the goal values for the input row using KNN from step02
    # We use the first 700 rows as training data for the estimation
    train_data = rows[:700]
    
    # Simple estimation: average of the goal values of the 5 nearest neighbors
    input_indices = [i for i, h in enumerate(header) if h[0].isupper() and i not in goals]
    
    distances = []
    for r in train_data:
        dist = sum((row[i] - r[i])**2 for i in input_indices)**0.5
        distances.append((dist, [r[g] for g in goals]))
    
    distances.sort(key=lambda x: x[0])
    top_k = distances[:5]
    
    # Estimated goal values
    estimates = [sum(d[1][i] for d in top_k) / len(top_k) for i in range(len(goals))]
    
    # Calculate how many rows this row is "better than"
    better_count = 0
    for r in rows:
        is_better = True
        for i, g_idx in enumerate(goals):
            val = r[g_idx]
            est = estimates[i]
            # If ends in +, higher is better. If -, lower is better.
            if header[g_idx].endswith('+'):
                if not (est >= val): is_better = False
            else:
                if not (est <= val): is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all teams based on its projected retention metrics."
    
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

    # Test with the last row, masking its goals
    test_row = list(rows[-1])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for g in goal_indices:
        test_row[g] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
