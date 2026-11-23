import csv
import random
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from step05 import blame

def race(header, rows, label):
    """
    Compares three strategies for finding the best row using a shared budget of 50 labels.
    """
    goal_col = next(c for c in header if c.endswith('+') or c.endswith('-'))
    goal_idx = header.index(goal_col)
    is_maximize = goal_col.endswith('+')
    
    # Shared budget
    budget = 50
    labeled_indices = {}
    
    def get_label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise ValueError("Budget exceeded")
            labeled_indices[i] = label(i)[0]
        return labeled_indices[i]

    def strategy_random(budget_per):
        indices = random.sample(range(len(rows)), budget_per)
        for i in indices: get_label(i)
        return max(indices, key=lambda i: labeled_indices[i]) if is_maximize else min(indices, key=lambda i: labeled_indices[i])

    def strategy_importance(budget_per):
        # Use blame logic to find important features, then sample based on those
        top_features = blame(header, rows[:100]) # Use a subset to find features
        # Simple heuristic: pick rows with high values in top features
        indices = sorted(range(len(rows)), key=lambda i: sum(rows[i][header.index(f)] for f in top_features if isinstance(rows[i][header.index(f)], (int, float))), reverse=is_maximize)[:budget_per]
        for i in indices: get_label(i)
        return max(indices, key=lambda i: labeled_indices[i]) if is_maximize else min(indices, key=lambda i: labeled_indices[i])

    def strategy_model(budget_per):
        # Active learning: sample, train, predict, pick next
        indices = random.sample(range(len(rows)), budget_per // 2)
        for i in indices: get_label(i)
        
        # Train model on current labels
        train_idx = list(labeled_indices.keys())
        df_train = pd.DataFrame([rows[i] for i in train_idx], columns=header)
        X = df_train.drop(columns=[goal_col])
        y = pd.Series([labeled_indices[i] for i in train_idx])
        
        # Simple encoding
        for col in X.columns:
            if X[col].dtype == 'object': X[col] = LabelEncoder().fit_transform(X[col].astype(str))
        
        model = RandomForestRegressor().fit(X, y)
        
        # Predict remaining and pick best
        X_all = pd.DataFrame(rows, columns=header).drop(columns=[goal_col])
        for col in X_all.columns:
            if X_all[col].dtype == 'object': X_all[col] = LabelEncoder().fit_transform(X_all[col].astype(str))
        
        preds = model.predict(X_all)
        best_idx = max(range(len(preds)), key=lambda i: preds[i]) if is_maximize else min(range(len(preds)), key=lambda i: preds[i])
        get_label(best_idx)
        return best_idx

    strategies = {
        "random": lambda: strategy_random(16),
        "importance": lambda: strategy_importance(16),
        "model": lambda: strategy_model(18)
    }
    
    results = {}
    for name, func in strategies.items():
        results[name] = func()
        
    best_strategy = max(results, key=lambda s: labeled_indices[results[s]]) if is_maximize else min(results, key=lambda s: labeled_indices[results[s]])
    
    return {"winner": best_strategy, "row": results[best_strategy], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(val) if header[i][0].isupper() else val for i, val in enumerate(row)])
            
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-'))
    
    def label(i): return [rows[i][goal_idx]]
    
    result = race(header, rows, label)
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
