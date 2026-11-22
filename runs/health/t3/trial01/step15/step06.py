import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against all other rows.
    Returns (p, reason) where p is the fraction of rows outperformed by the given row.
    """
    # Identify indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    # Prepare training data for estimation
    le = LabelEncoder()
    sym_idx = header.index('criterion')
    le.fit([r[sym_idx] for r in rows])
    
    def get_features(r):
        return [float(le.transform([r[sym_idx]])[0]) if i == sym_idx else float(r[i]) 
                for i in input_indices]

    X = [get_features(r) for r in rows]
    
    # Train models for each goal
    estimates = []
    for g_idx in goal_indices:
        y = [r[g_idx] for r in rows]
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        estimates.append(model.predict([get_features(row)])[0])
    
    # Calculate utility: -MRE + ACC + PRED40
    def get_utility(goals):
        # MRE is index 0 (ends in -), ACC is 1 (+), PRED40 is 2 (+)
        return -goals[0] + goals[1] + goals[2]
    
    target_utility = get_utility(estimates)
    all_utilities = [get_utility([r[g] for g in goal_indices]) for r in rows]
    
    # Calculate fraction of rows outperformed
    better_count = sum(1 for u in all_utilities if target_utility > u)
    p = better_count / len(rows)
    
    reason = f"This configuration is estimated to outperform {p:.1%} of all available setups based on its predicted multi-objective utility."
    
    return p, reason

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
                    processed_row.append(float(val))
            rows.append(processed_row)
    
    # Test with the first row as the 'unknown' setup
    test_row = rows[0][:]
    test_row[0] = "?"
    test_row[1] = "?"
    test_row[2] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Fraction outperformed: {p:.4f}")
    print(f"Justification: {reason}")
