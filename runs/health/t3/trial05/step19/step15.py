import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies which input columns have the least impact on performance (badness).
    Columns with low feature importance in a model predicting 'badness' are 
    candidates for factory defaults.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate a 'badness' score for each row
    # Normalize goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
    # Higher score = worse performance.
    def get_badness(row):
        score = 0
        for i in goal_indices:
            col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
            min_v, max_v = min(col_vals), max(col_vals)
            rng = max_v - min_v + 1e-9
            norm = (row[i] - min_v) / rng
            if header[i].endswith('-'):
                score += norm
            else:
                score += (1 - norm)
        return score

    badness_scores = [get_badness(row) for row in rows]
    
    # Prepare data for Random Forest
    X = []
    encoders = {}
    for i in input_indices:
        if isinstance(rows[0][i], str):
            le = LabelEncoder()
            le.fit([str(r[i]) for r in rows])
            encoders[i] = le
            
    for row in rows:
        feat = []
        for i in input_indices:
            if i in encoders:
                feat.append(encoders[i].transform([str(row[i])])[0])
            else:
                feat.append(float(row[i]))
        X.append(feat)
    
    # Train a regressor to predict badness
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, badness_scores)
    
    # Get feature importances
    importances = model.feature_importances_
    # Sort by importance ascending: least important are best for factory defaults
    indexed_importances = sorted(zip(importances, [header[i] for i in input_indices]))
    
    # Return the names of the input columns that least explain badness
    return [name for score, name in indexed_importances]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
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
        
        # The columns that least explain badness are the safest to set to defaults
        safe_settings = blame(header, rows)
        print("Settings that can be left at factory defaults (least impact on performance):")
        for col in safe_settings:
            print(f"- {col}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
