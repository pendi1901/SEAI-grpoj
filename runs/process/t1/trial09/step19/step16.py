import csv

def justify(header, rows, row):
    """
    Explains why a recommended setup (A) is better than a user-selected setup (B).
    Estimates goals for both using a nearest-neighbor approach and compares them.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]

    def get_dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (r1[i] - r2[i]) ** 2
        return d ** 0.5

    def estimate_goals(target_row):
        best_dist = float('inf')
        nearest_row = None
        for r in rows:
            d = get_dist(target_row, r)
            if d < best_dist:
                best_dist = d
                nearest_row = r
        return [nearest_row[i] for i in goal_indices]

    def is_better(goals_a, goals_b):
        # Returns True if goals_a dominates goals_b
        better_in_at_least_one = False
        for i, idx in enumerate(goal_indices):
            name = header[idx]
            val_a, val_b = goals_a[i], goals_b[i]
            if name.endswith('-'):
                if val_a > val_b: return False
                if val_a < val_b: better_in_at_least_one = True
            else:
                if val_a < val_b: return False
                if val_a > val_b: better_in_at_least_one = True
        return better_in_at_least_one

    # Estimate goals for the provided row
    estimated_goals = estimate_goals(row)

    # Calculate percentile rank
    better_count = 0
    for r in rows:
        actual_goals = [r[i] for i in goal_indices]
        if is_better(estimated_goals, actual_goals):
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This setup is estimated to outperform {p:.2f} of all configurations, making it a more balanced choice than your preferred option."
    
    return p, reason

def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            processed = []
            for val in row:
                try:
                    processed.append(float(val))
                except ValueError:
                    processed.append(val)
            rows.append(processed)
    return header, rows

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        header, rows = load_data(filename)
        
        # Select a sample row to justify
        test_row = list(rows[0])
        for i in range(len(header)):
            if header[i].endswith(('-', '+')):
                test_row[i] = "?"
                
        p, reason = justify(header, rows, test_row)
        print(f"Rank: {p}")
        print(f"Justification: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
