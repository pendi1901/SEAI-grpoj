import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that contribute most to poor performance.
    We define 'bad' rows as those in the bottom 25% of the score distribution.
    We then use feature importance from a Random Forest to see which inputs
    are most predictive of these low scores.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    min_cols = [c for c in header if c.endswith('-')]
    max_cols = [c for c in header if c.endswith('+')]
    input_cols = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    
    # Normalize goals to a single performance score [0, 1]
    scores = pd.DataFrame(index=df.index)
    for col in min_cols:
        c_min, c_max = df[col].min(), df[col].max()
        scores[col] = (c_max - df[col]) / (c_max - c_min + 1e-9)
    for col in max_cols:
        c_min, c_max = df[col].min(), df[col].max()
        scores[col] = (df[col] - c_min) / (c_max - c_min + 1e-9)
    
    df['score'] = scores.mean(axis=1)
    
    # Prepare features
    X = df[input_cols].copy()
    for col in input_cols:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
    
    # Train a model to predict the score
    # High importance features are those that drive the score (good or bad)
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X, df['score'])
    
    # Get feature importances
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Return the top 3 most influential columns
    return [input_cols[i] for i in indices[:3]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.train.csv'
    data = []
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
            data.append(processed_row)
            
    bad_drivers = blame(header, data)
    
    print("Analysis of performance drivers:")
    print("The settings that most significantly impact performance (and thus explain")
    print("why some setups perform poorly) are:")
    for col in bad_drivers:
        print(f"- {col}")
    print("\nThese columns have the highest influence on the outcome scores.")
