import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal columns.
    We use a Random Forest to rank feature importance and return the columns
    with the lowest importance scores.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Prepare data
    encoders = {}
    X = []
    # We aggregate goals into a single target for importance ranking
    # For simplicity, we use the first goal column
    target_idx = goal_indices[0]
    y = [float(row[target_idx]) for row in rows]
    
    for row in rows:
        processed_row = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                if i not in encoders:
                    encoders[i] = LabelEncoder()
                    encoders[i].fit([str(r[i]) for r in rows])
                processed_row.append(float(encoders[i].transform([str(val)])[0]))
            else:
                processed_row.append(float(val))
        X.append(processed_row)
        
    # Train model to find feature importance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get importances
    importances = list(zip(input_indices, model.feature_importances_))
    # Sort by importance ascending to find the ones that "have nothing to do" with the goal
    importances.sort(key=lambda x: x[1])
    
    # Return the names of the bottom 5 least important columns
    return [header[idx] for idx, imp in importances[:5]]

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

    useless_columns = blame(header, rows)
    
    print("Analysis: Which columns have little impact on employee tenure?")
    print("You may consider stopping the collection of these columns:")
    for col in useless_columns:
        print(f"- {col}")
