import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the single best change to a row's settings that improves its 
    Pareto ranking.
    """
    def get_score(r):
        # Heuristic: sum of normalized goals
        score = 0
        for i, name in enumerate(header):
            if name.endswith('-'):
                # Minimize: lower is better
                score += (1.0 - r[i])
            elif name.endswith('+'):
                # Maximize: higher is better
                score += r[i]
        return score

    best_change = {}
    best_score = -1.0
    
    # Try every allowed change for each lever
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != row[idx]]
        else:  # Numeric (low, high)
            low, high = allowed
            # Test boundaries and midpoint
            candidates = [low, high, (low + high) / 2.0]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            
            # Evaluate improvement
            score = get_score(new_row)
            if score > best_score:
                best_score = score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
            rows.append(processed_row)

    # Example: Fix the first row
    bad_row = rows[0]
    levers = {
        'N_estimators': (100, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Max_depth': (2, 12)
    }
    
    recommendation = fix(header, bad_row, levers)
    print("Recommendation to improve performance by changing one setting:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to {val}")
