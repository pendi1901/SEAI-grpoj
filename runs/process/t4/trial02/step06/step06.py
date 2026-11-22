import csv
import pandas as pd
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the goals for the given row, compares it against all rows,
    and returns the percentile rank and a justification.
    """
    # 1. Estimate the missing goals for the input row
    # guess() expects a list of rows, so we wrap our row
    # We need to handle the "?" in the row for the guess function
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Create a copy to avoid mutating the original
    test_row = list(row)
    
    # Predict all goals. Since step02.guess only predicts the first goal,
    # we iterate to predict all goals for the row.
    predicted_goals = []
    for goal in goals:
        # Temporarily set the target goal to the first goal for the guess function
        # or just use a simple KNN approach for all goals.
        # To keep it simple and consistent with step02:
        df_train = pd.DataFrame(rows, columns=header)
        from sklearn.neighbors import KNeighborsRegressor
        knn = KNeighborsRegressor(n_neighbors=5)
        knn.fit(df_train[inputs], df_train[goal])
        
        # Predict for the input row
        input_df = pd.DataFrame([test_row], columns=header)
        pred = knn.predict(input_df[inputs])[0]
        predicted_goals.append(pred)
    
    # 2. Calculate scores for all rows
    # We use the logic from step01 to rank
    all_data = rows + [test_row[:-len(goals)] + predicted_goals]
    df = pd.DataFrame(all_data, columns=header)
    
    normalized_goals = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        if goal.endswith('-'):
            normalized_goals[goal] = (col - col.min()) / (col.max() - col.min())
        else:
            normalized_goals[goal] = (col.max() - col) / (col.max() - col.min())
    
    df['score'] = normalized_goals.sum(axis=1)
    
    # 3. Calculate percentile
    target_score = df.iloc[-1]['score']
    better_than_count = (df['score'][:-1] > target_score).sum()
    p = better_than_count / len(rows)
    
    reason = f"This setup is better than {p:.1%} of all known configurations because its predicted performance metrics result in a lower aggregate cost-to-goal distance."
    
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        # Pick a sample row and mask its goals
        sample_row = rows[0][:]
        goals = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for g_idx in goals:
            sample_row[g_idx] = "?"
            
        p, reason = justify(header, rows, sample_row)
        print(f"Percentile: {p}")
        print(f"Justification: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
