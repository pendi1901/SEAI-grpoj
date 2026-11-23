import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor with OneHotEncoding for symbolic columns.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)

    # Identify goal columns and input columns
    goal_cols = [col for col in header if col.endswith('-') or col.endswith('+')]
    target_col = goal_cols[0]  # MRE-
    input_cols = [col for col in header if col not in goal_cols]

    # Identify numeric and categorical columns
    numeric_features = [col for col in input_cols if df_train[col].dtype != 'object']
    categorical_features = [col for col in input_cols if df_train[col].dtype == 'object']

    # Create a preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # Create a pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Train model
    X_train = df_train[input_cols]
    y_train = df_train[target_col]
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(df_test[input_cols])
    return predictions.tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                # Convert numeric columns, keep symbolic as strings
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split data for demonstration: 80% train, 20% test
    split_idx = int(len(rows) * 0.8)
    train_data = rows[:split_idx]
    test_data = rows[split_idx:]

    # Mask goals in test data
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    masked_test = []
    for row in test_data:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)

    predictions = guess(header, train_data, masked_test)
    
    print(f"Estimated MRE- for the first 5 test rows:")
    for i in range(min(5, len(predictions))):
        print(f"Row {i}: {predictions[i]:.4f}")
    print("...")
    print(f"Successfully generated {len(predictions)} forecasts.")
