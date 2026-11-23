import csv
from step08 import fix as step08_fix

def fix(header, row, levers):
    """
    Finds the best change to the provided levers to minimize 'Idle-'.
    We test small steps within the allowed ranges for each lever.
    """
    idle_idx = header.index('Idle-')

    def score_row(r):
        # We specifically want to minimize Idle-
        return float(r[idle_idx])

    best_score = score_row(row)
    recommendation = {}

    # Try changing each lever to a few points within its range
    for col_name, bounds in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        
        # Handle numeric levers (low, high)
        if isinstance(bounds, tuple):
            low, high = bounds
            for i in range(6):
                new_val = low + (high - low) * (i / 5.0)
                if new_val == row[idx]:
                    continue
                    
                test_row = list(row)
                test_row[idx] = new_val
                new_score = score_row(test_row)
                
                if new_score < best_score:
                    best_score = new_score
                    recommendation = {col_name: new_val}
        
        # Handle symbolic levers (list of strings)
        elif isinstance(bounds, list):
            for val in bounds:
                if val == row[idx]:
                    continue
                test_row = list(row)
                test_row[idx] = val
                new_score = score_row(test_row)
                
                if new_score < best_score:
                    best_score = new_score
                    recommendation = {col_name: val}
    
    return recommendation

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to floats, keep symbolic as strings
                processed = []
                for i, val in enumerate(row):
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(val)
                rows.append(processed)
            
            # Customer cannot hire (Team Size is fixed), so we look at other inputs
            # We exclude 'Team Size' from the levers
            levers = {
                'Culture': (0.0, 1.0),
                'Criticality': (0.0, 1.0),
                'Dynamism': (0.0, 1.0),
                'Size': (0.0, 1.0),
                'Plan': (0.0, 1.0)
            }
            
            # Find a "bad" row (high idle time)
            idle_idx = header.index('Idle-')
            bad_row = max(rows, key=lambda r: r[idle_idx])
            
            suggestion = fix(header, bad_row, levers)
            
            print("Customer Inquiry: I am not allowed to hire. What else can I change to cut idle time?")
            if suggestion:
                for col, val in suggestion.items():
                    print(f"Recommendation: Adjust '{col}' to {val if isinstance(val, str) else f'{val:.4f}'}.")
            else:
                print("No simple adjustment found to improve idle time without hiring.")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
