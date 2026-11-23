import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with high 'Idle-' values.
    We compare the top 10% worst rows (highest Idle-) against the rest.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    idle_idx = header.index('Idle-')
    
    # Sort rows by Idle- descending to find the worst
    sorted_rows = sorted(rows, key=lambda r: float(r[idle_idx]), reverse=True)
    
    # Take the worst 10%
    n = len(rows)
    worst = sorted_rows[:max(1, n // 10)]
    others = sorted_rows[max(1, n // 10):]
    
    # Calculate average for each input column in worst vs others
    # We look for inputs where the average in 'worst' is significantly higher or lower
    # than in 'others'.
    diffs = []
    for i in input_indices:
        w_vals = [float(r[i]) for r in worst]
        o_vals = [float(r[i]) for r in others]
        
        avg_w = sum(w_vals) / len(w_vals)
        avg_o = sum(o_vals) / len(o_vals)
        
        # We look for the largest absolute difference in normalized space
        diffs.append((abs(avg_w - avg_o), header[i]))
    
    # Return the top 2 inputs that explain the variance
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in diffs[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        explanations = blame(header, rows)
        print("The worst setups (high idle time) are primarily driven by:")
        for i, col in enumerate(explanations):
            print(f"{i+1}. {col}")
        print("These factors show the most significant deviation in setups with high idle time.")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
