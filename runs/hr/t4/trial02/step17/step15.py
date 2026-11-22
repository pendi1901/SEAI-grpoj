import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal 'YearsAtCompany+'.
    We use a Random Forest Regressor to calculate feature importances across the 
    entire dataset, identifying columns with the lowest predictive power.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify the goal column
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    
    # Identify input columns (exclude goals)
    inputs = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Encode all symbolic data to numeric for the model
    df_encoded = df.copy()
    for col in header:
        if df_encoded[col].dtype == 'object':
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            
    X = df_encoded[inputs]
    y = df_encoded[goal_col]
    
    # Use Random Forest to find feature importances
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get importances and sort ascending to find the least impactful
    importances = sorted(zip(inputs, model.feature_importances_), key=lambda x: x[1])
    
    # Return the names of the 5 least impactful columns
    return [name for name, score in importances[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    least_impactful = blame(header, rows)
    
    print("Analysis: Which columns have little to no impact on employee tenure?")
    print("The following columns have the lowest predictive power regarding tenure:")
    for col in least_impactful:
        print(f"- {col}")
    print("\nThese columns may be candidates for removal to simplify data collection.")
