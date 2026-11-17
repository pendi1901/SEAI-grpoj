import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that best explain short stays.
    'Worst' rows are defined as those with the lowest 'YearsAtCompany+'.
    We use a Random Forest to find feature importances for predicting tenure.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal and input columns
    target = 'YearsAtCompany+'
    inputs = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Prepare data
    df_clean = df.copy()
    le_map = {}
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            le = LabelEncoder()
            df_clean[col] = le.fit_transform(df_clean[col].astype(str))
            le_map[col] = le
            
    X = df_clean[inputs]
    y = df_clean[target]
    
    # Train a model to see what drives tenure
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = pd.Series(model.feature_importances_, index=inputs)
    top_features = importances.sort_values(ascending=False).head(3).index.tolist()
    
    return top_features

if __name__ == "__main__":
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Identify the factors
    factors = blame(header, rows)
    
    print("Analysis: What explains short stays in departments?")
    print(f"The primary factors influencing tenure duration are: {', '.join(factors)}.")
    print("These variables show the strongest correlation with how long an employee remains at the company.")
