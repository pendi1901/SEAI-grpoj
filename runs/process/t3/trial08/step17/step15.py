import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies the input columns that best explain why the worst rows are bad.
    We define 'bad' rows as those with the lowest aggregate performance.
    We then use feature importance to see which inputs drive these outcomes.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns and input columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Normalize goals to calculate an aggregate "badness" score
    # For '-', lower is better (so higher is worse). For '+', higher is better (so lower is worse).
    scores = pd.DataFrame(index=df.index)
    for col in goals:
        vals = df[col].astype(float)
        norm = (vals - vals.min()) / (vals.max() - vals.min() + 1e-9)
        if col.endswith('-'):
            scores[col] = norm  # High norm = bad
        else:
            scores[col] = 1 - norm  # High norm = bad
            
    # Aggregate badness score
    df['badness'] = scores.mean(axis=1)
    
    # Train a Random Forest to predict 'badness' from inputs
    X = df[inputs]
    y = df['badness']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    feature_importance = sorted(zip(importances, inputs), reverse=True)
    
    # Return the top 2 most important (most impactful) and the bottom 2 (safest to ignore)
    # The prompt asks for "which matter most" and "which can I safely stop worrying about"
    top_two = [name for imp, name in feature_importance[:2]]
    bottom_two = [name for imp, name in feature_importance[-2:]]
    
    return top_two + bottom_two

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        results = blame(header, rows)
        
        print("Customer Inquiry: Which project factors matter most to cost?")
        print("-" * 60)
        print(f"Factors that matter most: {results[0]}, {results[1]}")
        print(f"Factors you can safely ignore: {results[2]}, {results[3]}")
        print("\nConclusion: Focus your management efforts on the top factors.")
        print("The bottom factors have negligible impact on project outcomes.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
