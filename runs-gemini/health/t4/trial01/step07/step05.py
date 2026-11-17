import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with poor performance.
    We define 'bad' rows as those in the bottom 25% of the total score.
    We then use feature importance from a Random Forest to see which inputs
    predict the 'badness' of a row.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns and input columns
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if c not in goal_cols]
    
    # Calculate scores to identify 'bad' rows
    # Reuse logic: higher score is better, so lower score is worse
    min_cols = [c for c in header if c.endswith('-')]
    max_cols = [c for c in header if c.endswith('+')]
    scores = pd.DataFrame(index=df.index)
    for col in min_cols:
        col_min, col_max = df[col].min(), df[col].max()
        scores[col] = (col_max - df[col]) / (col_max - col_min + 1e-9)
    for col in max_cols:
        col_min, col_max = df[col].min(), df[col].max()
        scores[col] = (df[col] - col_min) / (col_max - col_min + 1e-9)
    
    df['total_score'] = scores.sum(axis=1)
    
    # Define bad rows as the bottom 25%
    threshold = df['total_score'].quantile(0.25)
    df['is_bad'] = (df['total_score'] <= threshold).astype(int)
    
    # Prepare features
    X = df[input_cols].copy()
    for col in X.columns:
        if X[col].dtype == 'object':
            X[col] = LabelEncoder().fit_transform(X[col].astype(str))
            
    # Train a regressor to predict 'badness'
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, df['is_bad'])
    
    # Get feature importances
    importances = pd.Series(model.feature_importances_, index=input_cols)
    # Return the top 3 columns that contribute to bad performance
    return importances.nlargest(3).index.tolist()

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row]
            data.append(processed_row)
            
    bad_factors = blame(header, data)
    
    print("Analysis: Which settings cause poor performance?")
    print(f"The settings most responsible for bad outcomes are: {', '.join(bad_factors)}.")
    print("These columns show the highest correlation with the lowest performing setups.")
