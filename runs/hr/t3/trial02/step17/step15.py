import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal columns.
    We train a Random Forest Regressor to predict the goal columns and 
    identify features with near-zero importance.
    """
    # Identify goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Prepare data
    X = []
    y = []
    
    # We aggregate goals into a single score for simplicity
    # Normalize goals: + is better high, - is better low
    for row in rows:
        processed_row = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple label encoding
                unique_vals = sorted(list(set(r[i] for r in rows)))
                processed_row.append(unique_vals.index(val))
            else:
                processed_row.append(val)
        X.append(processed_row)
        
        # Calculate a composite score for the row
        score = 0
        for g_idx in goal_indices:
            val = row[g_idx]
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        y.append(score)
    
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Map importances back to column names
    feature_importance_map = []
    for i, idx in enumerate(input_indices):
        feature_importance_map.append((header[idx], importances[i]))
    
    # Sort by importance ascending (least important first)
    feature_importance_map.sort(key=lambda x: x[1])
    
    # Return columns with very low importance (bottom 5)
    return [item[0] for item in feature_importance_map[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
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
    
    unimportant_factors = blame(header, rows)
    
    print("Analysis: Which columns have little impact on employee retention?")
    print("The following columns have the lowest predictive power and could potentially be removed:")
    for i, factor in enumerate(unimportant_factors, 1):
        print(f"{i}. {factor}")
    print("\nStrategy: These columns show the least correlation with the goal metrics, "
          "suggesting they are not critical for tracking employee tenure.")
