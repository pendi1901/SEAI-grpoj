import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies the two input columns that have the highest feature importance
    for predicting the 'Cost-' goal in the worst-performing rows.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (not goals)
    inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Identify the 'Cost-' goal
    target = 'Cost-'
    
    # Define "worst" rows: those with the highest 'Cost-' values
    # (Since Cost- is minimized, higher values are worse)
    threshold = df[target].quantile(0.75)
    worst_rows = df[df[target] >= threshold]
    
    # Use a Random Forest to find feature importance for 'Cost-'
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(worst_rows[inputs], worst_rows[target])
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Pair inputs with their importance scores
    feat_imp = sorted(zip(inputs, importances), key=lambda x: x[1], reverse=True)
    
    # Return the top 2 input columns that explain the cost
    return [feat_imp[0][0], feat_imp[1][0]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        important_factors = blame(header, rows)
        
        # Identify columns to stop worrying about (those not in the top 2)
        all_inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
        unimportant_factors = [col for col in all_inputs if col not in important_factors]
        
        print("Project Cost Analysis:")
        print(f"The factors that matter most to cost are: {', '.join(important_factors)}.")
        print(f"You can likely stop worrying about: {', '.join(unimportant_factors[:2])} (and others).")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
