import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies the input columns that matter most to the 'Cost-' goal.
    Returns the top 2 input columns that explain the worst-performing rows,
    and identifies the columns that can be safely ignored (those with the lowest importance).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input and goal columns
    inputs = [col for col in header if not (col.endswith(('-', '+')))]
    
    # We focus on 'Cost-' as the primary goal to minimize.
    # Worst rows are those with the highest Cost- values.
    worst_rows = df.nlargest(int(len(df) * 0.25), 'Cost-')
    
    # Use Random Forest to determine feature importance for 'Cost-'
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(worst_rows[inputs], worst_rows['Cost-'])
    
    # Get feature importances
    importances = dict(zip(inputs, model.feature_importances_))
    
    # Sort inputs by importance
    sorted_inputs = sorted(importances, key=importances.get, reverse=True)
    
    # Return the top 2 as the ones that matter most
    return sorted_inputs[:2]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        important_factors = blame(header, rows)
        
        # Identify the least important factors (the ones to stop worrying about)
        inputs = [col for col in header if not (col.endswith(('-', '+')))]
        all_importances = {col: 0 for col in inputs} # Placeholder logic
        # Re-run importance on full set to find least important
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(pd.DataFrame(rows, columns=header)[inputs], pd.DataFrame(rows, columns=header)['Cost-'])
        importances = dict(zip(inputs, model.feature_importances_))
        least_important = sorted(importances, key=importances.get)[:2]
        
        print("Customer Inquiry: Which project facts matter most to Cost-?")
        print(f"Most important factors to monitor: {', '.join(important_factors)}")
        print(f"Factors you can safely stop worrying about: {', '.join(least_important)}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
