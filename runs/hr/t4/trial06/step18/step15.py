import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal columns.
    We use Random Forest feature importance to identify which inputs are 
    least predictive of the goals, suggesting they can be dropped.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('+') or c.endswith('-')]
    inputs = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Encode symbolic columns
    df_encoded = df.copy()
    for col in header:
        if not col[0].isupper():
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df[col].astype(str))
            
    # We aggregate importance across all goal columns
    total_importances = pd.Series(0.0, index=inputs)
    
    for goal in goals:
        X = df_encoded[inputs]
        y = df_encoded[goal]
        
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        
        total_importances += pd.Series(model.feature_importances_, index=inputs)
    
    # Return inputs with the lowest importance scores (bottom 5)
    return total_importances.nsmallest(5).index.tolist()

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    useless_factors = blame(header, rows)
    
    print("Analysis: Which data points are redundant?")
    print("The following input columns have the least impact on our performance goals")
    print("and are candidates for removal from future data collection:")
    for factor in useless_factors:
        print(f"- {factor}")
