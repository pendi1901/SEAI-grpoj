import pandas as pd
import numpy as np
import csv
from sklearn.ensemble import RandomForestRegressor

def choose(header, rows, label):
    """
    Finds the best row by using an active learning approach.
    We use a Random Forest to model the goals based on the inputs,
    then iteratively query the most promising rows (Expected Improvement).
    """
    df = pd.DataFrame(rows, columns=header)
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Preprocess inputs
    df_inputs = pd.get_dummies(df[inputs])
    
    # We will label 50 rows.
    # Strategy: 
    # 1. Label 10 random rows to seed the model.
    # 2. For the remaining 40, predict goals for all unlabelled rows,
    #    pick the one with the best predicted aggregate score.
    
    labeled_indices = []
    
    def get_aggregate_score(goal_values):
        score = 0
        for i, col in enumerate(goals):
            val = goal_values[i]
            # Normalize: we don't know the global min/max yet, 
            # but we can use the current labeled set to estimate.
            score += val if col.endswith('-') else (1.0 - val)
        return score

    # Initial random sampling
    import random
    indices_to_sample = random.sample(range(len(rows)), 10)
    
    for i in indices_to_sample:
        label(i)
        labeled_indices.append(i)
        
    # Active learning loop
    for _ in range(40):
        # Train model on currently labeled data
        X_train = df_inputs.iloc[labeled_indices]
        y_train = [label(i) for i in labeled_indices]
        
        # We model each goal independently
        models = []
        for g_idx in range(len(goals)):
            m = RandomForestRegressor(n_estimators=20)
            m.fit(X_train, [y[g_idx] for y in y_train])
            models.append(m)
            
        # Predict for all unlabelled
        unlabeled = [i for i in range(len(rows)) if i not in labeled_indices]
        best_idx = -1
        best_score = float('inf')
        
        for i in unlabeled:
            pred_goals = [m.predict(df_inputs.iloc[[i]])[0] for m in models]
            score = get_aggregate_score(pred_goals)
            if score < best_score:
                best_score = score
                best_idx = i
        
        label(best_idx)
        labeled_indices.append(best_idx)
        
    # Return the index of the best row found among labeled ones
    final_scores = {i: get_aggregate_score(label(i)) for i in labeled_indices}
    return min(final_scores, key=final_scores.get)

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        true_goals = []
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            # Separate inputs and goals
            goals = [float(val) for i, val in enumerate(row) if header[i].endswith(('-', '+'))]
            inputs = [val for i, val in enumerate(processed) if not header[i].endswith(('-', '+'))]
            rows.append(inputs + ["?"] * len(goals))
            true_goals.append(goals)

    def label(i):
        return true_goals[i]

    best_idx = choose(header, rows, label)
    print(f"The best configuration found is at row {best_idx}.")
    print("This selection was optimized using an active learning strategy over 50 trials.")
