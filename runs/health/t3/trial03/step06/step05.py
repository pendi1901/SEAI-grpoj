import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies which input columns are most predictive of poor performance.
    We define 'bad' as the bottom 25% of rows based on a combined goal score.
    We then train a Random Forest to predict the 'badness' and report feature importances.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate a normalized score for each row to define 'badness'
    # Minimize '-' (multiply by -1), Maximize '+' (multiply by 1)
    def get_score(row):
        score = 0
        for i in goal_indices:
            direction = -1 if header[i].endswith('-') else 1
            score += row[i] * direction
        return score

    scores = [get_score(row) for row in rows]
    # Define bad rows as those with the lowest 25% of scores
    threshold = sorted(scores)[len(scores) // 4]
    is_bad = [1 if s <= threshold else 0 for s in scores]

    # Prepare input data (X)
    X = []
    encoders = {}
    for i in input_indices:
        if isinstance(rows[0][i], str):
            le = LabelEncoder()
            col_vals = [row[i] for row in rows]
            le.fit(col_vals)
            encoders[i] = le

    for row in rows:
        features = []
        for i in input_indices:
            if i in encoders:
                features.append(encoders[i].transform([row[i]])[0])
            else:
                features.append(row[i])
        X.append(features)

    # Train a regressor to find which inputs correlate with 'bad' outcomes
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, is_bad)

    # Get feature importances
    importances = model.feature_importances_
    indexed_importances = sorted(zip(importances, input_indices), reverse=True)
    
    # Return the names of the top 3 most influential input columns
    top_features = [header[idx] for _, idx in indexed_importances[:3]]
    return top_features

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
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

    bad_drivers = blame(header, rows)
    
    print("Analysis of poor performing setups:")
    print("The settings that contribute most to poor performance are:")
    for feature in bad_drivers:
        print(f"- {feature}")
    print("\nThese parameters show the strongest correlation with the worst-performing configurations.")
