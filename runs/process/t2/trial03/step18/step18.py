import csv
import step08

def fix(header, row, levers):
    """
    Finds the best change to a 'bad' row by testing adjustments 
    to the provided levers to minimize the goal score, specifically
    targeting 'Idle-' reduction.
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
    
    # Try adjusting each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        original_val = row[idx]
        
        # For numeric levers, test 10 points in the range
        if isinstance(allowed, (tuple, list)) and len(allowed) == 2:
            low, high = allowed[0], allowed[1]
            for i in range(11):
                test_val = low + (high - low) * (i / 10.0)
                row[idx] = test_val
                current_score = score_row(row)
                if current_score < best_score:
                    best_score = current_score
                    best_change = {col_name: test_val}
        
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
        
        # Identify a 'bad' row (high Idle- score)
        idle_idx = header.index('Idle-')
        bad_row_idx = max(range(len(rows)), key=lambda i: rows[i][idle_idx])
        bad_row = rows[bad_row_idx]
        
        # Customer cannot hire (Team Size is off-limits), suggest other levers
        levers = {
            'Culture': (0.0, 1.0),
            'Criticality': (0.0, 1.0),
            'Dynamism': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Plan': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        if recommendation:
            print("Analysis: To cut idle time without hiring, we recommend:")
            for col, val in recommendation.items():
                print(f"  Adjust '{col}' to {val:.4f}")
        else:
            print("No beneficial adjustments found within the provided constraints.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
