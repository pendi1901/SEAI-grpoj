import csv
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

def justify(header, rows, row):
    """
    Estimates the performance of a given row and returns its percentile rank
    among the existing rows, along with a justification.
    """
    df = pd.DataFrame(rows, columns=header)
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    input_cols = [col for col in header if col not in goal_cols]

    # 1. Estimate the goals for the target row using KNN
    X_train = df[input_cols]
    y_train = df[goal_cols]
    
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    # Extract inputs from the target row (ignoring "?")
    target_inputs = [row[i] for i, col in enumerate(header) if col in input_cols]
    estimated_goals = model.predict([target_inputs])[0]
    
    # 2. Calculate aggregate score for all rows
    # Normalize: 1 - (val - min)/(max - min) for '-', (val - min)/(max - min) for '+'
    def get_aggregate(data_row):
        scores = []
        for i, col in enumerate(header):
            if col in goal_cols:
                col_data = df[col]
                norm = (data_row[i] - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
                scores.append(1 - norm if col.endswith('-') else norm)
        return sum(scores) / len(scores)

    all_scores = [get_aggregate(r) for r in rows]
    
    # 3. Calculate target row score
    target_score = 0
    for i, col in enumerate(header):
        if col in goal_cols:
            col_data = df[col]
            norm = (estimated_goals[goal_cols.index(col)] - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
            target_score += (1 - norm if col.endswith('-') else norm)
    target_score /= len(goal_cols)
    
    # 4. Calculate percentile
    better_than = [s for s in all_scores if s < target_score]
    p = len(better_than) / len(all_scores)
    
    reason = f"This setup is estimated to perform better than {p:.1%} of all known configurations based on its input parameters."
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Test with the first row, masking its goals
        test_row = list(rows[0])
        for i, h in enumerate(header):
            if h.endswith(('-', '+')):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
