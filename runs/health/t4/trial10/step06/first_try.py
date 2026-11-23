import csv
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against all other rows.
    Returns (fraction of rows outperformed, explanation string).
    """
    # 1. Estimate the goal values for the target row
    # We use the guess function from step02, which uses a Random Forest
    # We need to pass the target row as a single-item list to guess()
    target_row = [row]
    estimated_goals = guess(header, rows, target_row)
    
    # 2. Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # 3. Compare target row against all rows in the dataset
    # A row is better if it is closer to the ideal for all goals
    def get_score(r):
        # We use the estimated goals for the target row, actuals for others
        vals = [estimated_goals[0] if i == goal_indices[0] else r[i] for i in range(len(header))]
        score = 0
        for i in goal_indices:
            col_data = [float(x[i]) for x in rows]
            min_v, max_v = min(col_data), max(col_data)
            norm = (vals[i] - min_v) / (max_v - min_v + 1e-9)
            score += norm if header[i].endswith('+') else (1 - norm)
        return score

    target_score = get_score(row)
    better_count = 0
    for r in rows:
        if get_score(r) < target_score:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This configuration is estimated to outperform {p:.1%} of all known setups based on its predicted performance metrics."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = [float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row]
                rows.append(processed_row)
        
        # Pick a sample row to justify, masking its goals
        sample_row = list(rows[0])
        for i in range(len(header)):
            if header[i].endswith(('-', '+')):
                sample_row[i] = '?'
        
        p, reason = justify(header, rows, sample_row)
        print(f"Performance Justification: {reason}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
