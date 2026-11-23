import csv

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with the 'Idle-' goal.
    We define 'worst' as rows in the top quartile of 'Idle-' values.
    We then calculate the correlation between each input and the 'Idle-' goal.
    """
    goal_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    # Sort rows by Idle- to find the worst ones
    sorted_rows = sorted(rows, key=lambda r: r[goal_idx], reverse=True)
    worst_rows = sorted_rows[:len(rows) // 4]
    
    # Calculate simple correlation: mean of input in worst rows vs mean of input in all rows
    # A high difference indicates that the input is a driver for the bad outcome
    scores = []
    for i in input_indices:
        all_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        worst_vals = [r[i] for r in worst_rows if isinstance(r[i], (int, float))]
        
        if not all_vals or not worst_vals:
            continue
            
        mean_all = sum(all_vals) / len(all_vals)
        mean_worst = sum(worst_vals) / len(worst_vals)
        
        # We look for inputs that deviate significantly in the worst setups
        diff = abs(mean_worst - mean_all)
        scores.append((diff, header[i]))
    
    # Return the top 2 inputs that explain the 'Idle-' behavior
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for diff, name in scores[:2]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        blame_factors = blame(header, rows)
        
        print("Analysis: Why do our worst setups leave so many people waiting around?")
        print(f"The primary drivers for high idle time are: {', '.join(blame_factors)}.")
        print("These inputs show the strongest correlation with the 'Idle-' goal in our worst-performing scenarios.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
