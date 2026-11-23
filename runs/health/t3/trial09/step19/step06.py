import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it to the dataset.
    Returns (fraction_better, reason_string).
    """
    df = pd.DataFrame(rows, columns=header)
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if c not in goal_cols]

    # Prepare training data and encode symbolic columns
    df_encoded = df.copy()
    encoders = {}
    for col in input_cols:
        if df_encoded[col].dtype == 'object':
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoders[col] = le
        else:
            df_encoded[col] = df_encoded[col].astype(float)

    X_train = df_encoded[input_cols]
    
    # Prepare target row
    row_df = pd.DataFrame([row], columns=header)
    X_test = row_df[input_cols].copy()
    for col in input_cols:
        if col in encoders:
            X_test[col] = encoders[col].transform(X_test[col].astype(str))
        else:
            X_test[col] = X_test[col].astype(float)

    # Estimate goals
    estimated_goals = {}
    for goal in goal_cols:
        y_train = df_encoded[goal]
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)
        estimated_goals[goal] = model.predict(X_test)[0]

    # Calculate score for target row
    row_score = 0
    for col in goal_cols:
        val = estimated_goals[col]
        row_score += val * (-1 if col.endswith('-') else 1)

    # Calculate scores for all historical rows
    def get_score(r):
        s = 0
        for col in goal_cols:
            val = r[header.index(col)]
            s += val * (-1 if col.endswith('-') else 1)
        return s

    all_scores = [get_score(r) for r in rows]
    better_count = sum(1 for s in all_scores if row_score > s)
    fraction = better_count / len(rows)
    
    reason = f"This setup is estimated to outperform {fraction:.1%} of all historical configurations based on its input parameters."
    return (float(fraction), reason)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Create a test row (using the first row's inputs, masking goals)
    test_row = rows[0][:]
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            test_row[i] = "?"

    p, reason = justify(header, rows, test_row)
    print(f"Performance Score: {p:.4f}")
    print(f"Justification: {reason}")
