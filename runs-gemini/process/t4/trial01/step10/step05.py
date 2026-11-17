import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with high 'Idle-' values.
    We use a Random Forest to rank feature importance for the 'Idle-' goal.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns and the target goal
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    input_cols = [header[i] for i in input_indices]
    target_col = 'Idle-'
    
    # Prepare data
    X = df[input_cols].astype(float)
    y = df[target_col].astype(float)
    
    # Use Random Forest to find feature importance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get top 3 features explaining the variance in 'Idle-'
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    top_features = [input_cols[i] for i in indices[:3]]
    return top_features

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    top_reasons = blame(header, rows)
    
    print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
    print("Analysis: The primary drivers for high idle time are:")
    for i, reason in enumerate(top_reasons):
        print(f"{i+1}. {reason}")
    print("\nThese input factors have the strongest influence on the 'Idle-' goal.")
