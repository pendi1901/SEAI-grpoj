import csv

def fix(header, row, levers):
    """
    Finds the best change to a 'bad' row by testing adjustments 
    to the provided levers to minimize the goal score.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def score_row(r):
        total = 0.0
        for idx in goal_indices:
            val = float(r[idx])
            if header[idx].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    best_change = {}
    best_score = score_row(row)
    found_improvement = False

    # Try adjusting each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        original_val = row[idx]
        
        # For numeric levers, test 10 points in the range
        if isinstance(allowed, tuple) or isinstance(allowed, list):
            low, high = allowed[0], allowed[1]
            for i in range(11):
                test_val = low + (high - low) * (i / 10.0)
                row[idx] = test_val
                current_score = score_row(row)
                if current_score < best_score:
                    best_score = current_score
                    best_change = {col_name: test_val}
                    found_improvement = True
        
        # Reset row
        row[idx] = original_val
        
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Identify a 'bad' row (high score)
        scored = []
        for i, row in enumerate(rows):
            total = sum(row[idx] if header[idx].endswith('-') else (1.0 - row[idx]) 
                        for idx in [j for j, n in enumerate(header) if n.endswith(('-', '+'))])
            scored.append((total, i))
        
        bad_row_idx = max(scored, key=lambda x: x[0])[1]
        bad_row = rows[bad_row_idx]
        
        # Define levers based on the problem context
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        if recommendation:
            print("Analysis: To rescue this project, we recommend the following adjustments:")
            for col, val in recommendation.items():
                print(f"  Change '{col}' to {val:.4f}")
            print("These changes are expected to improve project efficiency and reduce idle time.")
        else:
            print("No beneficial adjustments found within the provided levers.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
