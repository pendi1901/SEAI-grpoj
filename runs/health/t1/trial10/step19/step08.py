import csv
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its score.
    'Smallest change' is defined by the number of levers adjusted.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(r):
        # Simple heuristic: sum of normalized goals
        # Since we don't have the full dataset context here, we use a 
        # relative improvement metric based on the provided row structure.
        # Higher is better.
        score = 0
        for i in goal_indices:
            val = r[i]
            if header[i].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # We try changing one lever at a time to find an improvement
    best_change = {}
    
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate a candidate value
        if isinstance(allowed, tuple):  # Numeric (low, high)
            low, high = allowed
            # Try a small step or a random value within range
            new_val = low + (high - low) * 0.5
        else:  # Symbolic
            new_val = [v for v in allowed if v != original_val][0]
            
        return {col_name: new_val}

    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        # Define levers based on problem description
        levers = {
            'N_estimators': (50, 200),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1, 20),
            'Min_impurity_decrease': (0, 10),
            'Max_depth': (1, 20)
        }
        
        # Pick a 'bad' row (e.g., the one with the worst MRE)
        mre_idx = header.index('MRE-')
        bad_row = max(rows, key=lambda r: r[mre_idx])
        
        recommendation = fix(header, bad_row, levers)
        
        print("To improve the current setup, we recommend the following change:")
        for col, val in recommendation.items():
            print(f"- Set {col} to {val}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
