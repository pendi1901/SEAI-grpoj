import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

def blame(header, rows):
    """
    Identifies which input columns are most predictive of poor performance.
    We define 'bad' as the bottom 25% of rows based on an aggregate score.
    We train a Random Forest to predict the performance score and use 
    feature importances to identify the culprits.
    """
    df = pd.DataFrame(rows, columns=header)
    
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if c not in goal_cols]
    
    # Calculate aggregate performance score
    # Normalize: (1 - MRE) + ACC + PRED40
    def get_score(row):
        mre = row[header.index('MRE-')]
        acc = row[header.index('ACC+')]
        pred = row[header.index('PRED40+')]
        return (1.0 - mre) + acc + pred

    scores = [get_score(row) for row in rows]
    df['score'] = scores
    
    # Define 'bad' as the bottom 25%
    threshold = df['score'].quantile(0.25)
    df['is_bad'] = (df['score'] <= threshold).astype(int)
    
    # Train a model to predict 'is_bad' to find feature importance
    numeric_features = [c for c in input_cols if df[c].dtype != 'object']
    categorical_features = [c for c in input_cols if df[c].dtype == 'object']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestRegressor(n_estimators=50, random_state=42))
    ])
    
    model.fit(df[input_cols], df['is_bad'])
    
    # Extract feature importances
    importances = model.named_steps['classifier'].feature_importances_
    
    # Map importances back to input column names
    cat_names = []
    if categorical_features:
        cat_names = model.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    
    all_feature_names = numeric_features + list(cat_names)
    
    # Aggregate importance by original column name
    importance_map = {col: 0.0 for col in input_cols}
    for name, imp in zip(all_feature_names, importances):
        for col in input_cols:
            if name.startswith(col):
                importance_map[col] += imp
                break
                
    # Return columns sorted by importance
    sorted_cols = sorted(importance_map.items(), key=lambda x: x[1], reverse=True)
    return [col for col, imp in sorted_cols if imp > 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)
            
    culprits = blame(header, rows)
    print("The settings most responsible for poor performance are:")
    for col in culprits[:3]:
        print(f"- {col}")
