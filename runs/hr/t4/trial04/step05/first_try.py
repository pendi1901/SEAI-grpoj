import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that best explain short stays.
    'YearsAtCompany+' is a goal to maximize. We define 'worst' rows as those
    in the bottom 25% of 'YearsAtCompany+'. We then use a Random Forest
    feature importance to identify which inputs correlate with these short stays.
    """
    goal_col = 'YearsAtCompany+'
    df = pd.DataFrame(rows, columns=header)
    
    # Define "worst" as the bottom 25% of tenure
    threshold = df[goal_col].quantile(0.25)
    df['is_short_stay'] = (df[goal_col] <= threshold).astype(int)
    
    # Prepare features
    input_cols = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    X = df[input_cols].copy()
    y = df['is_short_stay']
    
    # Encode symbolic columns
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        else:
            X[col] = X[col].fillna(0)
            
    # Use Random Forest to find feature importance
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    # Get top 3 features
    importances = pd.Series(clf.feature_importances_, index=input_cols)
    top_features = importances.nlargest(3).index.tolist()
    
    return top_features

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    results = blame(header, rows)
    print("The primary factors explaining short employee tenure are:")
    for feature in results:
        print(f"- {feature}")
