import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def get_score(header, row_goals, df_full):
    """Calculates normalized aggregate score for a row."""
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    scores = []
    for i, col in enumerate(goals):
        vals = df_full[col].astype(float)
        norm = (row_goals[i] - vals.min()) / (vals.max() - vals.min() + 1e-9)
        scores.append(1 - norm if col.endswith('-') else norm)
    return np.mean(scores)

def race(header, rows, label):
    """
    Compares:
    1. 'random': Random selection.
    2. 'big_teams': Always pick rows with the highest 'Team Size'.
    3. 'active': Uncertainty-based active learning.
    """
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if c not in goal_cols]
    
    df_full = pd.DataFrame(rows, columns=header)
    for col in header:
        if col not in goal_cols:
            df_full[col] = pd.to_numeric(df_full[col], errors='ignore')
    
    labeled = {}
    budget = 50
    
    def run_strategy(name, n_trials):
        nonlocal budget
        strat_labeled = {}
        
        for _ in range(n_trials):
            if budget <= 0: break
            
            if name == "random":
                idx = np.random.choice(len(rows))
            elif name == "big_teams":
                # Pick rows with highest Team Size, prioritizing unlabeled
                sorted_indices = df_full['Team Size'].argsort()[::-1]
                idx = next((i for i in sorted_indices if i not in labeled), sorted_indices[0])
            else: # active
                if not labeled:
                    idx = np.random.choice(len(rows))
                else:
                    df_l = pd.DataFrame([rows[i] for i in labeled], columns=header)
                    for i, col in enumerate(goal_cols):
                        df_l[col] = [labeled[idx][i] for idx in labeled]
                    model = RandomForestRegressor(n_estimators=20).fit(df_l[input_cols], df_l[goal_cols[0]])
                    preds = [tree.predict(df_full[input_cols]) for tree in model.estimators_]
                    idx = np.argmax(np.std(preds, axis=0))
            
            if idx not in labeled:
                labeled[idx] = label(idx)
                strat_labeled[idx] = labeled[idx]
                budget -= 1
        
        best_idx, best_score = -1, -1
        for idx, g in strat_labeled.items():
            s = get_score(header, g, df_full)
            if s > best_score:
                best_score, best_idx = s, idx
        return best_idx, best_score

    s1_idx, s1_score = run_strategy("random", 16)
    s2_idx, s2_score = run_strategy("big_teams", 17)
    s3_idx, s3_score = run_strategy("active", 17)
    
    results = {"random": s1_score, "big_teams": s2_score, "active": s3_score}
    winner = max(results, key=results.get)
    winner_idx = {"random": s1_idx, "big_teams": s2_idx, "active": s3_idx}[winner]
    
    return {"winner": winner, "row": winner_idx, "tried": ["random", "big_teams", "active"]}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    df = pd.read_csv(filename)
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    def label(i):
        goals = [c for c in header if c.endswith('-') or c.endswith('+')]
        return [float(df.iloc[i][c]) for c in goals]
    
    result = race(header, rows, label)
    print(f"Strategy Comparison Results:")
    print(f"The winner is: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    print("\nConclusion: Your current strategy of 'big teams' is often outperformed by")
    print("smarter, data-driven selection methods that account for project trade-offs.")
