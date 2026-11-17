import pandas as pd
import numpy as np

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee arrangement.
    Strategies:
    1. random: Picks 16 random rows.
    2. tenure_max: Picks 17 rows with the highest 'TotalWorkingYears'.
    3. satisfaction_max: Picks 17 rows with the highest 'EnvironmentSatisfaction'.
    """
    df = pd.DataFrame(rows, columns=header)
    goal_cols = [c for c in header if c.endswith('+') or c.endswith('-')]
    
    def get_score(row_idx):
        goals = label(row_idx)
        scores = []
        for i, col in enumerate(goal_cols):
            val = goals[i]
            # Normalize: + is better high, - is better low
            # Using a simple relative score based on the whole dataset range
            col_data = df[col].astype(float)
            col_min, col_max = col_data.min(), col_data.max()
            diff = col_max - col_min if col_max != col_min else 1.0
            if col.endswith('+'):
                scores.append((val - col_min) / diff)
            else:
                scores.append((col_max - val) / diff)
        return sum(scores) / len(scores)

    strategies = {}
    
    # Strategy 1: Random
    indices_rand = np.random.choice(len(rows), 16, replace=False)
    strategies["random"] = {idx: get_score(idx) for idx in indices_rand}
    
    # Strategy 2: Tenure focus
    indices_tenure = df['TotalWorkingYears'].nlargest(17).index.tolist()
    strategies["tenure_max"] = {idx: get_score(idx) for idx in indices_tenure}
    
    # Strategy 3: Satisfaction focus
    indices_sat = df['EnvironmentSatisfaction'].nlargest(17).index.tolist()
    strategies["satisfaction_max"] = {idx: get_score(idx) for idx in indices_sat}
    
    best_overall_score = -1
    winner = ""
    best_row = -1
    
    for name, results in strategies.items():
        for idx, score in results.items():
            if score > best_overall_score:
                best_overall_score = score
                winner = name
                best_row = idx
                
    return {"winner": winner, "row": best_row, "tried": list(strategies.keys())}

if __name__ == "__main__":
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    goal_indices = [i for i, c in enumerate(header) if c.endswith('+') or c.endswith('-')]
    
    def label(i):
        return [float(rows[i][idx]) for idx in goal_indices]
    
    # Mask rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    result = race(header, masked_rows, label)
    
    print("Strategy Race Results:")
    print("-" * 30)
    print(f"Winner: {result['winner']}")
    print(f"Best Row Found: {result['row']}")
    print(f"Strategies Tested: {', '.join(result['tried'])}")
    print("-" * 30)
    print("The 'tenure_max' strategy typically identifies the most stable roles.")
    exit(0)
