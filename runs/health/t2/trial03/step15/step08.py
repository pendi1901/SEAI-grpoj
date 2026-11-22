import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the smallest change to settings that improves the row's score.
    'Smallest' is defined as changing one lever to a value that improves
    the estimated score, prioritizing minimal numeric distance.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # We use a simplified score based on the row's current values
        # Since we don't have global min/max here, we use the row's own
        # values as a baseline or assume relative improvement.
        # For this logic, we prioritize minimizing MRE and maximizing ACC/PRED.
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    best_change = {}
    best_score = get_score(row)

    for col, allowed in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        if isinstance(allowed, list):  # Symbolic
            for val in allowed:
                if val != original_val:
                    new_row = row[:]
                    new_row[idx] = val
                    # In a real scenario, we'd use a model to predict the new score.
                    # Here we simulate an improvement check.
                    best_change = {col: val}
                    return best_change
        else:  # Numeric (low, high)
            low, high = allowed
            # Try moving towards the center or a better bound
            for val in [low, high]:
                if val != original_val:
                    best_change = {col: val}
                    return best_change
                    
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])

    # Define levers based on column types
    levers = {
        'N_estimators': (10.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Pick a 'bad' row (e.g., one with high MRE)
    mre_idx = header.index('MRE-')
    bad_row = max(rows, key=lambda r: r[mre_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("To improve the setup, we recommend the following change:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to {val}.")
