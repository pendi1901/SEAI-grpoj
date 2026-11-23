import csv
import random

def fix(header, row, levers):
    """
    Finds the smallest change to levers to improve the row's goals.
    We perform a local search by perturbing the levers and picking the 
    one that results in the best improvement to the goal scores.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(r):
        scores = []
        for i in goal_indices:
            val = r[i]
            # Goals ending in '-' are minimized, '+' are maximized.
            # Since data is normalized [0,1], we treat 1 as best.
            if header[i].endswith('-'):
                scores.append(1.0 - val)
            else:
                scores.append(val)
        return sum(scores) / len(scores)

    best_change = {}
    best_score = get_score(row)
    
    # Try small perturbations for each lever
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate a few candidates for this lever
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            low, high = allowed
            # Try moving towards the middle or extremes
            for _ in range(5):
                candidates.append(random.uniform(low, high))
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            if val == original_val:
                continue
            
            new_row = list(row)
            new_row[idx] = val
            new_score = get_score(new_row)
            
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
            rows = [[float(x) for x in row] for row in reader]
        
        # Identify a "bad" row (e.g., high cost, high idle)
        # We define bad as having a score in the bottom 10%
        def get_score(r):
            goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
            scores = [1.0 - r[i] if header[i].endswith('-') else r[i] for i in goal_indices]
            return sum(scores) / len(scores)
        
        scores = [get_score(r) for r in rows]
        bad_idx = scores.index(min(scores))
        bad_row = rows[bad_idx]
        
        # Levers: Plan and Team Size are the primary knobs for staffing/planning
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Report: Project Rescue Plan")
        if recommendation:
            col, val = list(recommendation.items())[0]
            print(f"To improve project performance, we recommend adjusting '{col}' to {val:.4f}.")
            print("This change is designed to reduce idle time and optimize costs.")
        else:
            print("No simple adjustment to Plan or Team Size was found to improve the current setup.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
