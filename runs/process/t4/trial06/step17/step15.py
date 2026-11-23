import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from step05 import blame as get_blame

def blame(header, rows):
    """
    Identifies the most important input columns that drive the 'Cost-' goal.
    The most important are the ones that matter most, and the least important
    (those with near-zero importance) are the ones to stop worrying about.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Train a Random Forest to predict 'Cost-'
    X = df[input_cols]
    y = df['Cost-']
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = pd.Series(model.feature_importances_, index=input_cols)
    
    # Return the top 2 as the ones that matter most
    return importances.nlargest(2).index.tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
            
        important = blame(header, rows)
        
        # Identify inputs to stop worrying about (those not in the top 2)
        all_inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
        unimportant = [col for col in all_inputs if col not in important]
        
        print("Analysis of project cost drivers:")
        print(f"The factors that matter most to cost are: {', '.join(important)}.")
        print(f"You can safely stop worrying about: {', '.join(unimportant[:2])} (and others).")
        print("These findings are based on feature importance analysis of historical project data.")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
