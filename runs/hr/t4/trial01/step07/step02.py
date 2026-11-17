import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def guess(header, train, test):
    """Estimate YearsAtCompany+ (the first goal column) for each test row."""
    
    target_col = None
    for col in header:
        if col.endswith('+') or col.endswith('-'):
            target_col = col
            break
    
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Replace "?" with NaN so missing values are handled properly
    df_train = df_train.replace('?', float('nan')).infer_objects()
    df_test = df_test.replace('?', float('nan')).infer_objects()
    
    X_train = df_train.drop(columns=[target_col]).values
    y_train = df_train[target_col].values
    
    X_test = df_test.drop(columns=[target_col]).values
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test).tolist()
    return predictions


if __name__ == "__main__":
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    mid = len(rows) // 2
    predictions = guess(header, rows[:mid], rows[mid:])

    print(f"Predicted YearsAtCompany+ for {len(predictions)} new hires:")
    for i, p in enumerate(predictions):
        actual = df.iloc[mid + i]['YearsAtCompany+']
        print(f"  Predicted={p:.1f}, Actual={actual}")
