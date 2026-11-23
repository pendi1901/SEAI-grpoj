import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies input columns that best explain high 'Cost-' values.
    Returns the top 2 input columns that correlate with the worst performance.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (those not ending in - or +)
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # We want to explain 'Cost-'.
    target = 'Cost-'
    
    # Focus on the "worst" setups (those with high Cost- values)
    # We define "worst" as the top 20% of rows with the highest Cost-
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
    
    # Return the top 2 input columns that explain the variance in Cost-
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
        
        top_factors = blame(header, rows)
        
        print("Customer Inquiry: Which project factors matter most to cost?")
        print("Analysis: The following input factors are the primary drivers of high cost:")
        for i, col in enumerate(top_factors):
            print(f"  {i+1}. {col}")
        
        # Identify what can be ignored (the least important inputs)
        input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
        ignored = [col for col in input_cols if col not in top_factors]
        
        print(f"\nConclusion: You should focus on {', '.join(top_factors)}.")
        print(f"You can likely stop worrying about: {', '.join(ignored)}.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
