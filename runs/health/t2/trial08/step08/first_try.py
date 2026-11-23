import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row's settings that improves its score.
    'Smallest change' is defined as changing one lever to a value that 
    maximizes the score improvement.
    """
    def get_score(r):
        # Use the logic from step01 to score a single row
        # Since we need to score a single row, we simulate a small population
        # or just use the row's own values relative to its potential.
        # For simplicity, we calculate the score based on the row's own metrics.
        mre_idx = header.index('MRE-')
        acc_idx = header.index('ACC+')
        pred_idx = header.index('PRED40+')
        
        # Normalize goals (using dummy ranges based on typical data)
        # MRE: 0 to 1, ACC: 0 to 1, PRED: 0 to 1
        s1 = 1.0 - r[mre_idx]
        s2 = r[acc_idx]
        s3 = r[pred_idx]
        return (s1 + s2 + s3) / 3.0

    best_change = {}
    best_score = get_score(row)
    
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try all allowed values
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = allowed
        else:  # Numeric (low, high)
            # Try boundaries and midpoint
            candidates = [allowed[0], (allowed[0] + allowed[1]) / 2, allowed[1]]
            
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
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)] for row in reader]
        
        # Define levers based on the dataset
        levers = {
            'N_estimators': (50, 200),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1, 20),
            'Max_depth': (1, 20)
        }
        
        # Pick a 'bad' row (e.g., the one with the worst score)
        # For demonstration, we pick the last row
        bad_row = rows[-1]
        recommendation = fix(header, bad_row, levers)
        
        print("Recommendation for improvement:")
        if recommendation:
            for col, val in recommendation.items():
                print(f"Change '{col}' to {val}")
        else:
            print("No single lever change found to improve performance.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
