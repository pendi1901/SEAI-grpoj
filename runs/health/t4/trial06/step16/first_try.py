import csv
from step02 import guess
from step01 import remember

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
    def get_score(r):
        score = 0
        for idx, direction in goals:
            col_data = [float(row_i[idx]) for row_i in rows]
            min_v, max_v = min(col_data), max(col_data)
            val = float(r[idx])
            norm = (val - min_v) / (max_v - min_v + 1e-9)
            score += norm if direction == 1 else (1 - norm)
        return score

    # Calculate target score using estimated goals
    target_score = 0
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for i, g_idx in enumerate(goal_indices):
        val = estimated_goals[i]
        col_data = [float(r[g_idx]) for r in rows]
        min_v, max_v = min(col_data), max(col_data)
        norm = (val - min_v) / (max_v - min_v + 1e-9)
        target_score += norm if header[g_idx].endswith('+') else (1 - norm)

    better_count = 0
    for r in rows:
        if get_score(r) < target_score:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"Using the biggest, deepest setup is not always optimal because this configuration is estimated to outperform only {p:.1%} of all known setups."
    
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

    # Define a "biggest, deepest" setup
    # N_estimators max is 200, Max_depth max is 12
    test_row = [0.0, 0.0, 0.0, 200.0, 'squared_error', 1.0, 1.0, 12.0]
    # Hide goals
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(reason)
