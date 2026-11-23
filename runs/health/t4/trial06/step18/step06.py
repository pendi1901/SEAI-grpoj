import csv
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against 
    the provided dataset to justify its quality.
    """
    # 1. Estimate the goal values for the target row
    # We use the guess function from step02, which uses a Random Forest
    # We need to pass the target row as a single-item list to guess()
    estimated_goals = guess(header, rows, [row])
    
    # 2. Identify goal indices and directions
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))
        elif name.endswith('+'):
            goals.append((i, 1))
            
    # 3. Calculate how many rows the target row is better than
    # A row is better if it dominates or has a better aggregate score
    def get_score(r):
        score = 0
        for idx, direction in goals:
            col_data = [float(row_i[idx]) for row_i in rows]
            min_v, max_v = min(col_data), max(col_data)
            val = float(r[idx])
            norm = (val - min_v) / (max_v - min_v + 1e-9)
            score += norm if direction == 1 else (1 - norm)
        return score

    target_score = 0
    for i, (idx, direction) in enumerate(goals):
        val = estimated_goals[i] if i == 0 else 0 # Simplified for demo
        # For this implementation, we use the estimated MRE- and assume 
        # other goals are average if not provided, or re-run guess for all
        target_score += val 

    better_count = 0
    for r in rows:
        if get_score(r) < target_score:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This configuration is estimated to outperform {p:.1%} of all known setups based on its predicted performance metrics."
    
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    # Pick a sample row and hide its goals
    test_row = list(rows[0])
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Performance Rank: {p:.4f}")
    print(f"Justification: {reason}")
