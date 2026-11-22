import csv

def fix(header, row, levers):
    """
    Finds the single best lever change to improve the row's performance.
    We evaluate potential changes by calculating the average goal improvement
    of rows in the dataset that match the proposed new setting.
    """
    # We need the global dataset to evaluate improvements.
    # Since the harness calls fix(header, row, levers), we must rely on 
    # the data being accessible. We will read it inside the function 
    # or assume it's available. To be safe and compliant, we read it here.
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_file = next(reader)
        for r in reader:
            rows.append([val if header_file[i] == 'criterion' else float(val) 
                         for i, val in enumerate(r)])

    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    def get_score(r):
        # Higher score is better: minimize MRE-, maximize others.
        s = 0
        for i in goal_indices:
            col = header[i]
            if col.endswith('-'):
                s -= r[i]
            else:
                s += r[i]
        return s

    best_change = {}
    best_improvement = -float('inf')

    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        
        candidates = []
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)):
            for val in allowed:
                if val != row[col_idx]:
                    candidates.append(val)
        else:
            low, high = allowed
            candidates = [low, (low + high) / 2, high]

        for val in candidates:
            # Find rows that have this setting to estimate performance
            matches = [r for r in rows if r[col_idx] == val]
            if not matches:
                continue
            
            avg_score = sum(get_score(r) for r in matches) / len(matches)
            improvement = avg_score - get_score(row)
            
            if improvement > best_improvement:
                best_improvement = improvement
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) 
                         for i, val in enumerate(row)])

    levers = {
        'N_estimators': (50.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    mre_idx = header.index('MRE-')
    bad_row = max(rows, key=lambda r: r[mre_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("To improve your setup with a single change, we recommend:")
    for col, val in recommendation.items():
        print(f"  Set '{col}' to {val}")
