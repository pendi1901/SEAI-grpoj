import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that are least predictive of 'bad' performance.
    If a column has low feature importance in predicting bad outcomes, 
    it suggests that changing it doesn't significantly impact the 
    likelihood of a poor result, making it a candidate for factory defaults.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Define 'bad' as the bottom 25% of rows based on a combined goal score
    def get_score(row):
        score = 0
        for i in goal_indices:
            direction = -1 if header[i].endswith('-') else 1
            score += row[i] * direction
        return score

    scores = [get_score(row) for row in rows]
    threshold = sorted(scores)[len(scores) // 4]
    is_bad = [1 if s <= threshold else 0 for s in scores]

    # Prepare input data (X)
    X = []
    encoders = {}
    for i in input_indices:
        if isinstance(rows[0][i], str):
            le = LabelEncoder()
            le.fit([row[i] for row in rows])
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
    
    # Sort by importance ascending (least important = safest to leave at default)
    indexed_importances = sorted(zip(importances, input_indices))
    
    # Return the names of the input columns that have the least impact
    return [header[idx] for _, idx in indexed_importances]

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

    safe_settings = blame(header, rows)
    
    print("Analysis: Which settings can be left at factory defaults?")
    print("The following settings have the least impact on performance,")
    print("making them the safest to leave at their factory defaults:")
    for i, feature in enumerate(safe_settings):
        print(f"{i+1}. {feature}")
