import csv
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-stakes project.
    We prioritize 'Size' and 'Criticality' as proxies for project scale/risk,
    then use a surrogate model to optimize within the 50-label budget.
    """
    # 1. Identify high-stakes rows (Large Size and High Criticality)
    df = pd.DataFrame(rows, columns=header)
    # Normalize inputs to find rows that are "large" and "critical"
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    
    # Score rows by size and criticality (higher is more "large/damaging")
    risk_scores = (df.iloc[:, size_idx] + df.iloc[:, crit_idx])
    
    # Pick 25 high-risk rows and 25 random rows to sample
    high_risk_indices = risk_scores.nlargest(25).index.tolist()
    random_indices = np.random.choice([i for i in range(len(rows)) if i not in high_risk_indices], 25, replace=False)
    indices_to_label = high_risk_indices + random_indices.tolist()
    
    # 2. Label the samples
    train_inputs = []
    train_goals = []
    input_cols = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    for i in indices_to_label:
        train_inputs.append([rows[i][j] for j in input_cols])
        train_goals.append(label(i))
        
    # 3. Train surrogate model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(train_inputs, train_goals)
    
    # 4. Predict and select best
    all_inputs = [[rows[i][j] for j in input_cols] for i in range(len(rows))]
    predictions = model.predict(all_inputs)
    
    # Score predictions (using logic from step01)
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    pred_df = pd.DataFrame(predictions, columns=[header[i] for i in goal_indices])
    scores = pd.DataFrame(index=pred_df.index)
    
    for col in pred_df.columns:
        col_data = pred_df[col]
        norm = (col_data - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
        scores[col] = 1 - norm if col.endswith('-') else norm
        
    aggregate_scores = scores.mean(axis=1)
    return int(aggregate_scores.idxmax())

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith(('-', '+')):
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        processed.append(float(val))
                rows.append(processed)
                true_goals.append(goals)
        
        def label(i):
            return true_goals[i]
            
        best_idx = choose(header, rows, label)
        print(f"Analysis complete. The best setup for a large, high-stakes project is at index {best_idx}.")
        print("This was determined by sampling high-risk configurations and modeling performance.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
