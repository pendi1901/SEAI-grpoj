import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using a Random Forest, then compares it
    to the historical 'rows' to determine its percentile rank.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Prepare training data for the model
    X = []
    encoders = {}
    for i in input_indices:
        if isinstance(rows[0][i], str):
            le = LabelEncoder()
            le.fit([r[i] for r in rows])
            encoders[i] = le
            
    def transform_row(r):
        return [encoders[i].transform([r[i]])[0] if i in encoders else r[i] for i in input_indices]

    X_train = [transform_row(r) for r in rows]
    
    # Estimate each goal
    estimated_goals = []
    for g_idx in goal_indices:
        y_train = [r[g_idx] for r in rows]
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)
        estimated_goals.append(model.predict([transform_row(row)])[0])
    
    # Calculate how many rows are worse than our estimated row
    # A row is better if MRE- is lower, ACC+ is higher, PRED40+ is higher
    def is_better(r_est, r_actual):
        # r_est is [MRE, ACC, PRED]
        # r_actual is the full row
        mre_better = r_est[0] <= r_actual[goal_indices[0]]
        acc_better = r_est[1] >= r_actual[goal_indices[1]]
        pred_better = r_est[2] >= r_actual[goal_indices[2]]
        return mre_better and acc_better and pred_better

    better_count = sum(1 for r in rows if is_better(estimated_goals, r))
    p = better_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all historical configurations based on its input parameters."
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
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Test with the last row as a sample
    test_row = rows[-1][:]
    for i in range(len(header)):
        if header[i].endswith('-') or header[i].endswith('+'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(reason)
    exit(0)
