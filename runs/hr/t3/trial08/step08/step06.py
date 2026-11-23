import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row relative to the dataset.
    A row is 'better' if its goal columns (ending in +) are higher than others.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    symbolic_indices = [i for i, name in enumerate(header) if not name[0].isupper()]
    
    # Prepare data for regression
    X = []
    y = []
    # We focus on the first goal column for ranking as per previous steps
    target_idx = goal_indices[0]
    
    encoders = {}
    for i in symbolic_indices:
        encoders[i] = LabelEncoder()
        all_vals = [r[i] for r in rows]
        encoders[i].fit(all_vals)

    def process(r):
        features = []
        for i, val in enumerate(r):
            if i in goal_indices: continue
            if i in symbolic_indices:
                features.append(float(encoders[i].transform([val])[0]))
            else:
                features.append(float(val))
        return features

    for r in rows:
        X.append(process(r))
        y.append(float(r[target_idx]))

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Predict the value for the input row
    pred = model.predict([process(row)])[0]
    
    # Calculate fraction of rows that this row is better than
    # Higher value is better for '+' columns
    better_count = sum(1 for r in rows if pred > r[target_idx])
    p = better_count / len(rows)
    
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all teams because its predicted tenure is {pred:.1f} years, which outperforms most other configurations in our records."
    
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Test with the first row, masking its goal columns
    test_row = rows[0][:]
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = '?'
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Justification: {reason}")
