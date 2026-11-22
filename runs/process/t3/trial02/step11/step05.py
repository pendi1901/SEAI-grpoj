import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with high 'Idle-' values.
    'Idle-' is a goal to minimize, so 'worst' rows are those with high Idle- values.
    We use a Random Forest to rank feature importance for predicting Idle-.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goals and inputs
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Target: Idle-
    target = 'Idle-'
    
    # Prepare data
    X = df[inputs]
    y = df[target]
    
    # Train a Random Forest to find feature importance
    # We use a simple regressor to see which inputs drive the Idle- value
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X, y)
    
    # Get feature importances
    importances = rf.feature_importances_
    
    # Pair names with importance scores
    feat_importances = sorted(zip(inputs, importances), key=lambda x: x[1], reverse=True)
    
    # Return the top 3 inputs that explain the variance in Idle-
    return [feat[0] for feat in feat_importances[:3]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        top_blames = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
        print("Analysis: The primary factors contributing to high idle time are:")
        for i, factor in enumerate(top_blames, 1):
            print(f"{i}. {factor}")
        print("\nThese inputs have the strongest influence on the 'Idle-' goal.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
