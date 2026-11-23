import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies which input columns contribute most to poor performance.
    We define 'bad' as the bottom 20% of rows based on a weighted goal score.
    We then train a classifier to predict the 'badness' and extract feature importances.
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
            # Fill numeric NaNs with mean, ensuring we don't touch object columns
            X[col] = X[col].fillna(X[col].mean())
            
    y = df['is_bad']
    
    # Use Random Forest to find which inputs correlate with being 'bad'
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    
    importances = sorted(zip(input_cols, clf.feature_importances_), key=lambda x: x[1], reverse=True)
    
    # Return the top 3 inputs that explain the bad performance
    return [name for name, score in importances[:3]]

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
            
    bad_factors = blame(header, rows)
    print("The settings most responsible for poor performance are:")
    for factor in bad_factors:
        print(f"- {factor}")
