import csv
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def blame(header, rows):
    """
    Identifies input columns that best explain short stays (low YearsAtCompany+).
    We use a Random Forest to predict 'YearsAtCompany+' and extract feature importances.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]
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

    X = encode([ [row[i] for i in input_indices] for row in rows ])
    y = [row[target_idx] for row in rows]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances and map back to column names
    importances = model.feature_importances_
    features = [(importances[i], header[input_indices[i]]) for i in range(len(input_indices))]
    features.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 3 most influential input columns
    return [f[1] for f in features[:3]]

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
            
    top_factors = blame(header, rows)
    
    print("Analysis: What explains why some employees have short stays?")
    print("The most influential factors identified are:")
    for factor in top_factors:
        print(f"- {factor}")
    print("\nThese input columns show the strongest correlation with tenure duration.")
