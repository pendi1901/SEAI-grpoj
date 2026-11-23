import csv
import step01
import step06

def fix(header, row, levers):
    """
    Finds the best change to a bad row by testing all lever values
    and picking the one that results in the best estimated performance.
    """
    best_change = {}
    best_score = float('inf')
    
    # We need a reference to all rows to use step06's justify/estimation logic
    # Since we don't have access to the full dataset here, we assume the 
    # harness or the caller provides the context. 
    # Given the constraints, we iterate through levers and pick the one 
    # that minimizes the score.
    
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Test each allowed value
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            # Test mid-point or bounds
            candidates = [allowed[0], (allowed[0] + allowed[1]) / 2, allowed[1]]
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            row[idx] = val
            # Use step06 logic to score the row
            score = step06.get_score(header, row)
            if score < best_score:
                best_score = score
                best_change = {col_name: val}
        
        # Reset row
        row[idx] = original_val
        
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        # Define levers based on the problem domain
        # Plan is 0-1, Team Size is 0-1
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        # Find a "bad" row (e.g., high cost, high idle)
        # Using step01 logic to find a bad one (highest score)
        goal_indices = [i for i, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
        
        def get_score(r):
            return sum(r[i] if header[i].endswith('-') else (1.0 - r[i]) for i in goal_indices)
        
        bad_row = max(rows, key=get_score)
        
        recommendation = fix(header, bad_row, levers)
        
        print("To rescue this project, we recommend the following changes:")
        for col, val in recommendation.items():
            print(f"- Adjust {col} to {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
