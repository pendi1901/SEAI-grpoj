import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows.
    To simulate requirements changing twice as fast, we adjust the 
    'Dynamism' input in the test set to double its value (capped at 1.0)
    before prediction.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    target_col = goals[0]
    
    # Simulate requirements changing twice as fast:
    # We modify the 'Dynamism' input for the test set.
    if 'Dynamism' in df_test.columns:
        df_test['Dynamism'] = (df_test['Dynamism'] * 2).clip(upper=1.0)
    
    # Train model
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(df_train[inputs], df_train[target_col])
    
    # Predict
    predictions = rf.predict(df_test[inputs])
    return predictions.tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        # Split: First half is stable, second half is "changing twice as fast"
        mid = len(rows) // 2
        train_data = rows[:mid]
        test_data = [row[:] for row in rows[mid:]]
        
        # Mask goals in test
        goals = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for row in test_data:
            for g_idx in goals:
                row[g_idx] = "?"
        
        estimates = guess(header, train_data, test_data)
        
        avg_est = sum(estimates) / len(estimates)
        print("Customer Inquiry: What happens to Cost- if requirements change twice as fast?")
        print(f"Analysis: By simulating a doubling of 'Dynamism' in the second half of the project,")
        print(f"the model estimates an average Cost- of {avg_est:.4f}.")
        print("Increased dynamism typically forces the model to predict higher costs due to")
        print("the overhead of managing rapid requirement shifts.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
