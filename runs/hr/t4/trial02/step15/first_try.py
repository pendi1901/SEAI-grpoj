import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal 'YearsAtCompany+'.
    We define 'worst' as the bottom 25% of tenure and use Random Forest feature 
    importance to identify which inputs are irrelevant (lowest importance).
    """
    df = pd.DataFrame(rows, columns=header)
    goal = 'YearsAtCompany+'
    
    # Identify input columns (exclude goals)
    inputs = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Encode symbolic data
    df_encoded = df.copy()
    for col in header:
        if df_encoded[col].dtype == 'object':
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            
    # Focus on the worst 25% of rows (short stays)
    threshold = df[goal].quantile(0.25)
    worst_rows = df_encoded[df[goal] <= threshold]
    
    X = worst_rows[inputs]
    y = worst_rows[goal]
    
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
    print("The following columns have the lowest predictive power regarding short stays:")
    for col in least_impactful:
        print(f"- {col}")
    print("\nThese columns may be candidates for removal to simplify data collection.")
