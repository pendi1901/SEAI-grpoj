import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies which input columns contribute least to the 'badness' of a row.
    If a column has low importance in predicting 'bad' performance, it suggests
    that changing it doesn't significantly impact the outcome, meaning it can
    likely be left at factory defaults.
    """
    df = pd.DataFrame(rows, columns=header)
    
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if c not in goal_cols]
    
    # Calculate a normalized score for each row to identify 'bad' ones
    # Minimize '-' (invert) and Maximize '+'
    scores = []
    for _, row in df.iterrows():
        s = 0
        for col in goal_cols:
            val = row[col]
            if col.endswith('-'):
                s -= val
            else:
                s += val
        scores.append(s)
    
    df['score'] = scores
    # Threshold for 'bad' (bottom 20%)
    threshold = df['score'].quantile(0.2)
    df['is_bad'] = (df['score'] <= threshold).astype(int)
    
    # Prepare features
    X = df[input_cols].copy()
    for col in input_cols:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        else:
            X[col] = X[col].fillna(X[col].mean())
            
    y = df['is_bad']
    
    # Use Random Forest to find which inputs correlate with being 'bad'
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    
    # Get feature importances
    importances = list(zip(input_cols, clf.feature_importances_))
    # Sort by importance ascending: the least important are the ones that 
    # don't affect performance much (safe to leave at default)
    importances.sort(key=lambda x: x[1])
    
    return [name for name, score in importances]

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
            
    safe_settings = blame(header, rows)
    print("Settings that can likely be left at factory defaults (least impact on performance):")
    for setting in safe_settings:
        print(f"- {setting}")
