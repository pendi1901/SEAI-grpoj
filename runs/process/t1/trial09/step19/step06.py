import csv

def justify(header, rows, row):
    """
    Estimates the goals for the given row using a nearest-neighbor approach,
    then calculates the percentile rank of this row against all other rows.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]

    def get_dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (r1[i] - r2[i]) ** 2
        return d ** 0.5

    # Estimate goals for the input row using the nearest neighbor
    best_dist = float('inf')
    nearest_row = None
    for r in rows:
        d = get_dist(row, r)
        if d < best_dist:
            best_dist = d
            nearest_row = r
    
    estimated_goals = [nearest_row[i] for i in goal_indices]

    def is_better(goals_a, goals_b):
        # Returns True if goals_a is better than goals_b
        for i, idx in enumerate(goal_indices):
            name = header[idx]
            if name.endswith('-'):
                if goals_a[i] > goals_b[i]: return False
            else:
                if goals_a[i] < goals_b[i]: return False
        return True

    # Compare estimated goals against all rows
    better_count = 0
    for r in rows:
        actual_goals = [r[i] for i in goal_indices]
        if is_better(estimated_goals, actual_goals):
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This setup is estimated to outperform {p:.1%} of all configurations based on its input parameters."
    return p, reason

def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(x) for x in row] for row in reader]
    return header, rows

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    header, rows = load_data(filename)
    
    # Create a test row (masking goals)
    test_row = list(rows[0])
    for i in range(len(header)):
        if header[i].endswith(('-', '+')):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p}")
    print(f"Justification: {reason}")
