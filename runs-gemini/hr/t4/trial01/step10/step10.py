import pandas as pd
import numpy as np
import random
from step01 import remember
from step05 import blame

def get_score(header, row, goal_indices):
    """Calculates a normalized score for a row based on goal columns."""
    score = 0
    for idx in goal_indices:
        val = row[idx]
        col_name = header[idx]
        if col_name.endswith('+'):
            score += val
        elif col_name.endswith('-'):
            score -= val
    return score

def race(header, rows, label):
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    # Strategies: 
    # 1. random: pick 50 random rows
    # 2. top_tenure: pick 50 rows with highest 'YearsAtCompany+' (using blame/heuristic)
    # 3. diverse: pick 50 rows spread across the dataset
    
    strategies = ["random", "top_tenure", "diverse"]
    budget = 50
    per_strategy = budget // len(strategies)
    
    results = {}
    best_overall_score = -float('inf')
    winner = None
    best_row_idx = -1
    
    # Strategy 1: Random
    indices_random = random.sample(range(len(rows)), per_strategy)
    
    # Strategy 2: Top Tenure (Heuristic: pick rows with high YearsAtCompany)
    # Since we don't know the values, we pick rows based on high 'TotalWorkingYears' as a proxy
    twy_idx = header.index('TotalWorkingYears')
    indices_top = sorted(range(len(rows)), key=lambda i: rows[i][twy_idx], reverse=True)[:per_strategy]
    
    # Strategy 3: Diverse (Spaced out)
    indices_diverse = [int(i) for i in np.linspace(0, len(rows)-1, per_strategy)]
    
    strategy_map = {"random": indices_random, "top_tenure": indices_top, "diverse": indices_diverse}
    
    for name, indices in strategy_map.items():
        local_best_score = -float('inf')
        local_best_idx = -1
        
        for idx in indices:
            true_goals = label(idx)
            # Update row with true goals
            for i, g_idx in enumerate(goal_indices):
                rows[idx][g_idx] = true_goals[i]
            
            score = get_score(header, rows[idx], goal_indices)
            if score > local_best_score:
                local_best_score = score
                local_best_idx = idx
        
        if local_best_score > best_overall_score:
            best_overall_score = local_best_score
            best_row_idx = local_best_idx
            winner = name
            
    return {"winner": winner, "row": best_row_idx, "tried": strategies}

if __name__ == "__main__":
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    def label(i):
        # Real data access
        df_orig = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
        return [df_orig.iloc[i, g_idx] for g_idx in goal_indices]
    
    outcome = race(header, rows, label)
    
    print(f"The winning strategy is: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
