import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row relative to the dataset.
    Returns (p, reason) where p is the fraction of rows this row outperforms.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    feature_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Encode data for regression
    encoders = {}
    def encode(data):
        encoded = []
        for r in data:
            new_r = []
            for i in feature_indices:
                val = r[i]
                if isinstance(val, str):
                    if i not in encoders:
                        le = LabelEncoder()
                        le.fit([x[i] for x in rows])
                        encoders[i] = le
                    new_r.append(encoders[i].transform([val])[0])
                else:
                    new_r.append(val)
            encoded.append(new_r)
        return encoded

    X = encode(rows)
    
    # Estimate goals for the input row
    estimates = []
    for g_idx in goal_indices:
        y = [r[g_idx] for r in rows]
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        estimates.append(model.predict([encode([row])[0]])[0])
    
    # Calculate how many rows this row is "better than"
    # Better = higher for '+', lower for '-'
    better_count = 0
    for r in rows:
        is_better = True
        for i, g_idx in enumerate(goal_indices):
            val_r = r[g_idx]
            val_est = estimates[i]
            if header[g_idx].endswith('+'):
                if not (val_est >= val_r): is_better = False
            else:
                if not (val_est <= val_r): is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"Based on your team's inputs, this arrangement is estimated to outperform {p:.1%} of existing staff records in retention metrics."
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)
    
    # Test with the first row, masking goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
