import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies the input columns that most influence the 'Cost-' goal.
    Returns the top two most important features and the two least important features.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (not goals)
    input_cols = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    target = 'Cost-'
    
    # Train a Random Forest to determine feature importance
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(df[input_cols], df[target])
    
    # Pair features with their importance scores
    importances = sorted(zip(input_cols, model.feature_importances_), key=lambda x: x[1], reverse=True)
    
    # Return top 2 (matter most) and bottom 2 (safely stop worrying about)
    # The prompt asks for "one or two facts... and which can I safely stop worrying about"
    # We return the top 2 and bottom 2 as a list of 4 names.
    top_two = [name for name, score in importances[:2]]
    bottom_two = [name for name, score in importances[-2:]]
    
    return top_two + bottom_two

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        results = blame(header, rows)
        
        print("Customer Inquiry: Which project facts matter most to 'Cost-', and which can I stop worrying about?")
        print(f"Analysis: The factors that matter most (highest impact) are: {results[0]} and {results[1]}.")
        print(f"Analysis: The factors you can safely stop worrying about (lowest impact) are: {results[2]} and {results[3]}.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
