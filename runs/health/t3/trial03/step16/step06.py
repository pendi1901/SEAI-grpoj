import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row and compares it to the dataset.
    Returns (p, reason) where p is the fraction of rows worse than the input,
    and reason is a human-readable explanation.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Encode symbolic data
    encoders = {}
    for i in input_indices:
        if isinstance(rows[0][i], str):
            le = LabelEncoder()
            le.fit([r[i] for r in rows])
            encoders[i] = le

    def transform(r):
        return [encoders[i].transform([r[i]])[0] if i in encoders else r[i] for i in input_indices]

    # Train models to predict each goal
    X = [transform(r) for r in rows]
    predictions = []
    for g_idx in goal_indices:
        y = [r[g_idx] for r in rows]
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        predictions.append(model.predict([transform(row)])[0])

    # Calculate score: minimize '-' (negate), maximize '+' (keep)
    def get_score(goals):
        score = 0
        for i, val in enumerate(goals):
            direction = -1 if header[goal_indices[i]].endswith('-') else 1
            score += val * direction
        return score

    target_score = get_score(predictions)
    all_scores = [get_score([r[i] for i in goal_indices]) for r in rows]
    
    # Fraction of rows worse than target
    worse_count = sum(1 for s in all_scores if target_score > s)
    p = worse_count / len(rows)
    
    reason = f"This configuration is estimated to outperform {p:.1%} of all known setups based on its predicted goal metrics."
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if val.replace('.', '', 1).isdigit() or (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) else val for val in row]
            rows.append(processed_row)

    # Test with the last row, masking its goals
    test_row = list(rows[-1])
    for i in range(len(test_row)):
        if header[i].endswith('-') or header[i].endswith('+'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(reason)
