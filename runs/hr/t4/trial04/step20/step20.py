import csv
import random
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def race(header, rows, label):
    """
    Compares the customer's rule of thumb (pay rises to newest staff)
    against a random strategy and a model-based strategy.
    """
    goal_col = next(c for c in header if c.endswith('+') or c.endswith('-'))
    goal_idx = header.index(goal_col)
    is_maximize = goal_col.endswith('+')
    
    budget = 50
    labeled_indices = {}
    
    def get_label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                return None
            labeled_indices[i] = label(i)[0]
        return labeled_indices[i]

    # Helper to encode data safely
    def encode_df(df):
        df_encoded = df.copy()
        for col in df_encoded.columns:
            if df_encoded[col].dtype == 'object':
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            else:
                df_encoded[col] = df_encoded[col].astype(float)
        return df_encoded

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        for i in indices: get_label(i)
        return max(indices, key=lambda i: labeled_indices[i]) if is_maximize else min(indices, key=lambda i: labeled_indices[i])

    # Strategy 2: Rule of Thumb (Give biggest pay rises to newest staff)
    def strategy_rule_of_thumb():
        indices = sorted(range(len(rows)), key=lambda i: (rows[i][header.index('YearsAtCompany+')], -rows[i][header.index('PercentSalaryHike')]))[:16]
        for i in indices: get_label(i)
        return max(indices, key=lambda i: labeled_indices[i]) if is_maximize else min(indices, key=lambda i: labeled_indices[i])

    # Strategy 3: Model-based
    def strategy_model():
        indices = random.sample(range(len(rows)), 18)
        for i in indices: get_label(i)
        
        train_idx = list(labeled_indices.keys())
        df_train = pd.DataFrame([rows[i] for i in train_idx], columns=header)
        X = df_train.drop(columns=[goal_col])
        y = pd.Series([labeled_indices[i] for i in train_idx])
        
        X_encoded = encode_df(X)
        model = RandomForestRegressor(n_estimators=50).fit(X_encoded, y)
        
        X_all = pd.DataFrame(rows, columns=header).drop(columns=[goal_col])
        X_all_encoded = encode_df(X_all)
        
        preds = model.predict(X_all_encoded)
        best_idx = max(range(len(preds)), key=lambda i: preds[i]) if is_maximize else min(range(len(preds)), key=lambda i: preds[i])
        get_label(best_idx)
        return best_idx

    results = {
        "random": strategy_random(),
        "rule_of_thumb": strategy_rule_of_thumb(),
        "model": strategy_model()
    }
    
    best_strategy = max(results, key=lambda s: labeled_indices[results[s]]) if is_maximize else min(results, key=lambda s: labeled_indices[results[s]])
    
    return {"winner": best_strategy, "row": results[best_strategy], "tried": list(results.keys())}

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
    print(f"Comparison Result: The '{result['winner']}' strategy performed best.")
    print(f"The rule of thumb (pay rises to newest) was compared against random and model-based search.")
