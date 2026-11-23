import csv
import random

def fix(header, row, levers):
    """
    Finds the smallest change to levers to improve the row's goals.
    We evaluate the impact of changing each lever to its bounds or 
    midpoints to find an improvement.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(r):
        scores = []
        for i in goal_indices:
            val = r[i]
            # Goals ending in '-' are minimized (1-val), '+' are maximized (val).
            # Data is normalized [0,1].
            if header[i].endswith('-'):
                scores.append(1.0 - val)
            else:
                scores.append(val)
        return sum(scores) / len(scores)

    best_change = {}
    best_score = get_score(row)
    
    # Iterate through each lever and test potential values
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            low, high = allowed
            # Test boundaries and midpoint
            candidates = [low, (low + high) / 2.0, high]
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            new_score = get_score(new_row)
            
            # We look for any improvement
            if new_score > best_score:
                best_score = new_score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        # Define a bad row (e.g., lowest score)
        def get_score(r):
            goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
            scores = [1.0 - r[i] if header[i].endswith('-') else r[i] for i in goal_indices]
            return sum(scores) / len(scores)
        
        scores = [get_score(r) for r in rows]
        bad_idx = scores.index(min(scores))
        bad_row = rows[bad_idx]
        
        # Levers based on the problem description
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Report: Project Rescue Plan")
        if recommendation:
            for col, val in recommendation.items():
                print(f"Recommended change: Set '{col}' to {val:.4f}.")
        else:
            print("No improvement found with current levers.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
