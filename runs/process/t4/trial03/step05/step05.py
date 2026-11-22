import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are bad.
    Uses feature importance from a Random Forest trained to predict the 'Idle-' goal.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns and the target goal
    inputs = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    target = 'Idle-'
    
    # Focus on the worst 25% of rows based on the 'Idle-' goal
    # Higher 'Idle-' is worse
    worst_rows = df.nlargest(int(len(df) * 0.25), target)
    
    # Train a simple model to see what drives the 'Idle-' value in these bad rows
    X = worst_rows[inputs]
    y = worst_rows[target]
    
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Pair features with importance scores
    feat_imp = sorted(zip(inputs, importances), key=lambda x: x[1], reverse=True)
    
    # Return the top 2 features that explain the 'Idle-' variance
    return [feat[0] for feat in feat_imp[:2]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        explanations = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
        print(f"Analysis: The primary drivers for high idle time in your worst setups are: {', '.join(explanations)}.")
        print("These input parameters have the strongest correlation with the 'Idle-' goal in your underperforming data.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
