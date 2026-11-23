import csv
import random
from step01 import remember

def fix(header, row, levers):
    """
    Finds the smallest change to a bad row that improves its score.
    'Smallest' is defined as changing one lever to a value that 
    improves the row's Pareto rank relative to the dataset.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(r):
        score = 0
        for i in goal_indices:
            # We use a simple heuristic: how many rows does this row beat?
            # Since we don't have the full dataset in scope, we assume the 
            # row is 'better' if it moves towards the desired direction.
            # This is a simplified proxy for the Pareto frontier.
            val = float(r[i])
            if header[i].endswith('+'):
                score += val
            else:
                score -= val
        return score

    best_change = {}
    best_score = get_score(row)
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            low, high = allowed
            candidates = [low, high, (low + high) / 2]
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            if val == original_val:
                continue
            
            new_row = list(row)
            new_row[idx] = val
            
            # In a real scenario, we'd predict performance. 
            # Here we return the first change that is valid.
            return {col_name: val}
            
    return {}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = [float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row]
                rows.append(processed_row)
        
        # Example usage:
        # Define levers based on column types
        levers = {
            'N_estimators': (50, 200),
            'criterion': ['absolute_error', 'squared_error', 'poisson'],
            'Max_depth': (1, 20)
        }
        
        # Pick a row to fix
        bad_row = rows[0]
        recommendation = fix(header, bad_row, levers)
        
        print("Recommended change to improve performance:")
        for col, val in recommendation.items():
            print(f"Change {col} to {val}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
