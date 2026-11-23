import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember

def justify(header, rows, row):
    """
    Estimates the performance of a given row and returns its percentile rank
    relative to the provided dataset.
    """
    df = pd.DataFrame(rows, columns=header)
    inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    goals = [col for col in header if col.endswith(('-', '+'))]

    # Estimate missing goals for the input row
    predictions = {}
    for goal in goals:
        model = KNeighborsRegressor(n_neighbors=5)
        model.fit(df[inputs], df[goal])
        predictions[goal] = model.predict([row[:len(inputs)]])[0]

    # Calculate aggregate score for all rows
    def get_aggregate(data_df):
        scores = pd.DataFrame(index=data_df.index)
        for goal in goals:
            col_min, col_max = data_df[goal].min(), data_df[goal].max()
            norm = (data_df[goal] - col_min) / (col_max - col_min + 1e-9)
            scores[goal] = (1 - norm) if goal.endswith('-') else norm
        return scores.mean(axis=1)

    all_scores = get_aggregate(df)
    
    # Calculate score for the input row
    row_df = pd.DataFrame([list(row[:len(inputs)]) + [predictions[g] for g in goals]], columns=header)
    row_score = get_aggregate(row_df).iloc[0]

    # Calculate percentile (fraction of rows that are worse than this one)
    p = (all_scores < row_score).mean()
    
    reason = f"This setup is better than {p:.1%} of all known configurations based on its estimated performance across all goals."
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        # Take the first row as a test case, masking its goals
        test_row = rows[0][:len(header) - 3] + ['?'] * 3
        
        p, reason = justify(header, rows, test_row)
        
        print(f"Justification: {reason}")
        print(f"Rank: {p:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
