import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies the top 2 input columns that most influence the 'Cost-' goal.
    The customer wants to know what matters most (high importance) and what 
    they can stop worrying about (low importance).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (not ending in - or +)
    inputs = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    target = 'Cost-'
    
    # Train a Random Forest to find feature importance regarding Cost-
    X = df[inputs]
    y = df[target]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    feat_imp = sorted(zip(inputs, importances), key=lambda x: x[1], reverse=True)
    
    # Return the top 2 most important features
    return [feat[0] for feat in feat_imp[:2]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float
                processed_row = [float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row]
                rows.append(processed_row)
        
        important_features = blame(header, rows)
        
        print("Customer Inquiry: What matters most for project cost?")
        print(f"Analysis: The two factors that most significantly impact your project cost are: {', '.join(important_features)}.")
        print("You should focus your management efforts on these parameters.")
        print("Any input columns not listed here have significantly less impact and can be deprioritized.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
