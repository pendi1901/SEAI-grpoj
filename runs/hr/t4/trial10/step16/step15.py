import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies input columns that have the least influence on the goal columns.
    We use a Random Forest to calculate feature importances and return the 
    names of the input columns with the lowest importance scores.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    def encode(data):
        encoded = []
        for row in data:
            new_row = []
            for i, val in enumerate(row):
                if isinstance(val, str):
                    new_row.append(hash(val) % 1000)
                else:
                    new_row.append(val)
            encoded.append(new_row)
        return np.array(encoded)

    # We use the first goal column as the target for importance analysis
    target_idx = goal_indices[0]
    
    X = encode([[row[i] for i in input_indices] for row in rows])
    y = [row[target_idx] for row in rows]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Pair importances with column names
    features = [(importances[i], header[input_indices[i]]) for i in range(len(input_indices))]
    
    # Sort by importance ascending (least important first)
    features.sort(key=lambda x: x[0])
    
    # Return the names of the input columns that have the least impact
    # We return the bottom 5 as candidates for removal
    return [f[1] for f in features[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    useless_columns = blame(header, rows)
    
    print("Analysis: Which columns have little impact on employee retention?")
    print("The following input columns have the lowest predictive power and could potentially be removed:")
    for col in useless_columns:
        print(f"- {col}")
    print("\nThese columns show minimal correlation with the goal metrics.")
