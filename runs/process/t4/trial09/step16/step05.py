import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that best explain high 'Idle-' values.
    Uses a Random Forest feature importance approach on the worst 20% of rows.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input and goal columns
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # We want to explain 'Idle-'.
    target = 'Idle-'
    
    # Focus on the "worst" setups (those with high Idle- values)
    # We define "worst" as the top 20% of rows with the highest Idle-
    threshold = df[target].quantile(0.8)
    worst_rows = df[df[target] >= threshold]
    
    # Use Random Forest to find feature importance for the target
    X = worst_rows[input_cols]
    y = worst_rows[target]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Pair features with importance scores
    feat_imp = sorted(zip(input_cols, importances), key=lambda x: x[1], reverse=True)
    
    # Return the top 3 input columns that explain the variance in Idle-
    return [feat[0] for feat in feat_imp[:3]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        top_blame = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
        print("Analysis: The following input factors are the primary drivers of high idle time:")
        for i, col in enumerate(top_blame):
            print(f"  {i+1}. {col}")
        print("\nThese factors contribute most significantly to the variance in 'Idle-' within our worst-performing setups.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
