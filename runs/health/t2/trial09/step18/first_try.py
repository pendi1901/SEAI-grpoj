import csv
from step01 import remember
from step08 import fix as base_fix

def fix(header, row, levers):
    """
    Recommends a single change to a 'bad' row to improve its performance.
    Uses the logic from step08.py to evaluate potential improvements.
    """
    return base_fix(header, row, levers)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) 
                         for i, val in enumerate(row)])

    # Identify a 'bad' row (one not in the top 5%)
    top_indices = remember(header, rows)
    all_indices = set(range(len(rows)))
    bad_indices = list(all_indices - set(top_indices))
    
    if bad_indices:
        bad_row = rows[bad_indices[0]]
        
        # Define allowed levers for the customer
        levers = {
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'N_estimators': (10.0, 200.0),
            'Min_sample_leaves': (1.0, 20.0),
            'Max_depth': (1.0, 20.0)
        }

        recommendation = fix(header, bad_row, levers)
        
        print("Optimization Analysis:")
        if recommendation:
            col, val = list(recommendation.items())[0]
            print(f"To improve your setup, we recommend changing '{col}' to {val}.")
        else:
            print("No single change was found that would improve your setup's performance.")
    else:
        print("No bad rows found to optimize.")
