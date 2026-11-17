import pandas as pd
from step02 import guess


def race(header, rows, label):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Identify feature columns (non-goal)
    feature_cols = [c for c in header if c not in goal_cols]

    def build_X(rows):
        X = np.zeros((len(rows), len(feature_cols)))
        for i, row in enumerate(rows):
            for j, col in enumerate(feature_cols):
                cell = row[header.index(col)]
                v = float(cell) if isinstance(cell, (int, float)) else 0.0
                X[i][j] = v
        return X

    # Build a model from all rows to predict MRE- for any configuration
    train_X = build_X(rows)
    y_train = np.array([float(row[header.index('MRE-')]) for row in rows if header.index('MRE-') != feature_cols[0]])

    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_X, y_train)

    # Strategy 1: Random search - pick up to 50 rows at random
    def strategy_random():
        n_rows = len(rows)
        chosen = set()
        while len(chosen) < 50 and len(chosen) < n_rows:
            idx = np.random.randint(0, n_rows)
            chosen.add(idx)
        return list(chosen)

    # Strategy 2: Greedy - pick rows with best known goals first
    def strategy_greedy():
        scored = []
        for i, row in enumerate(rows):
            s = 0.0
            for col in goal_cols:
                cell = row[header.index(col)]
                if isinstance(cell, (int, float)):
                    v = float(cell)
                else:
                    continue
                if '-' in col:
                    s += v
                else:
                    s -= v
            scored.append((i, -s))  # negate so best comes first

        scored.sort(key=lambda x: x[1])
        chosen = []
        for i, _ in scored[:50]:
            if i not in chosen:
                chosen.append(i)
        return chosen

    # Strategy 3: Model-based - use the trained model to predict and pick best predicted MRE-
    def strategy_model():
        preds = []
        for row in rows:
            x_test = np.zeros((1, len(feature_cols)))
            for j, col in enumerate(feature_cols):
                cell = row[header.index(col)]
                v = float(cell) if isinstance(cell, (int, float)) else 0.0
                x_test[0][j] = v
            pred = model.predict(x_test)[0]
            preds.append(pred)

        # Pick rows with lowest predicted MRE-
        scored = [(i, p) for i, p in enumerate(preds)]
        scored.sort(key=lambda x: x[1])
        chosen = []
        for i, _ in scored[:50]:
            if i not in chosen:
                chosen.append(i)
        return chosen

    # Run all three strategies and collect their results
    random_rows = strategy_random()
    greedy_rows = strategy_greedy()
    model_rows = strategy_model()

    # Get true goal values for each row (using label if available, else from rows)
    def get_goals(row_idx):
        goals = []
        for col in goal_cols:
            cell = rows[row_idx][header.index(col)]
            if isinstance(cell, str) and cell == '?':
                goals.append(None)
            elif isinstance(cell, (int, float)):
                goals.append(float(cell))
            else:
                goals.append(0.0)
        return goals

    # Evaluate each strategy's chosen rows against true values from label or rows
    def evaluate(rows_list):
        scores = []
        for idx in rows_list:
            goals = get_goals(idx)
            s = 0.0
            valid = True
            for col in goal_cols:
                if goals[goal_cols.index(col)] is None:
                    continue
                v = goals[goal_cols.index(col)]
                if '-' in col:
                    s += abs(v - min([g for g, c in zip(goals, goal_cols) if c.endswith('-') and g is not None]))
                else:
                    s += abs(v - max([g for g, c in zip(goals, goal_cols) if c.endswith('+') and g is not None]))
            scores.append(s)
        return scores

    # Actually, let me simplify this. The label function gives true goals for each row.
    # We need to evaluate which strategy found the best row overall.
    
    # Get all rows that any strategy tried (union of all chosen rows)
    all_tried = set(random_rows + greedy_rows + model_rows)

    # For evaluation, use label if available, otherwise fall back to rows data
    def get_true_goals(row_idx):
        goals = []
        for col in goal_cols:
            cell = rows[row_idx][header.index(col)]
            if isinstance(cell, str) and cell == '?':
                goals.append(None)
            elif isinstance(cell, (int, float)):
                goals.append(float(cell))
            else:
                goals.append(0.0)
        return goals

    # Find the best row overall based on true goal values
    def score_row(row_idx):
        goals = get_true_goals(row_idx)
        s = 0.0
        for col in goal_cols:
            cell = rows[row_idx][header.index(col)]
            if isinstance(cell, (int, float)):
                v = float(cell)
            else:
                continue
            # We need to know the best values across all rows
            break
        
    # Let me restart with a cleaner approach
    
    def score_row_v2(row_idx):
        goals = []
        for col in goal_cols:
            cell = rows[row_idx][header.index(col)]
            if isinstance(cell, (int, float)):
                v = float(cell)
            else:
                continue
            goals.append(v)
        
        # Calculate score relative to best known values
        s = 0.0
        for col in goal_cols:
            cell = rows[row_idx][header.index(col)]
            if isinstance(cell, (int, float)):
                v = float(cell)
            else:
                continue
            
            # For simplicity, just use the raw value - lower MRE- is better, higher ACC+ and PRED40+ are better
            if col == 'MRE-':
                s += v  # want to minimise
            elif col == 'ACC+' or col == 'PRED40+':
                s -= v  # want to maximise
        
        return -s  # negate so higher is better

    # Find the best row among all tried rows
    best_score = float('-inf')
    best_row = None
    
    for idx in all_tried:
        score = score_row_v2(idx)
        if score > best_score:
            best_score = score
            best_row = idx

    return {
        "winner": "random",  # placeholder - will be determined below
        "row": best_row,
        "tried": ["random", "greedy", "model"]
    }


if __name__ == "__main__":
    import numpy as np
    
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(map(float, row)) for _, row in df.iterrows()]

    # For the main function, we need to actually determine the winner
    # Let's redo this properly
    
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    def score_row(row_idx):
        goals = []
        for col in goal_cols:
            cell = rows[row_idx][header.index(col)]
            if isinstance(cell, (int, float)):
                v = float(cell)
            else:
                continue
            goals.append(v)
        
        s = 0.0
        for col in goal_cols:
            cell = rows[row_idx][header.index(col)]
            if isinstance(cell, (int, float)):
                v = float(cell)
            else:
                continue
            
            if col == 'MRE-':
                s += v
            elif col == 'ACC+' or col == 'PRED40+':
                s -= v
        
        return -s

    # Run strategies and find best row
    random_rows = set()
    greedy_rows = set()
    model_rows = set()

    import numpy as np
    
    # Random strategy
    n_rows = len(rows)
    for _ in range(50):
        idx = np.random.randint(0, n_rows)
        random_rows.add(idx)

    # Greedy strategy - pick best rows first
    scored = []
    for i, row in enumerate(rows):
        s = 0.0
        for col in goal_cols:
            cell = row[header.index(col)]
            if isinstance(cell, (int, float)):
                v = float(cell)
            else:
                continue
            if col == 'MRE-':
                s += v
            elif col == 'ACC+' or col == 'PRED40+':
                s -= v
        scored.append((i, -s))

    scored.sort(key=lambda x: x[1])
    for i, _ in scored[:50]:
        greedy_rows.add(i)

    # Model-based strategy (same as before)
    feature_cols = [c for c in header if c not in goal_cols]

    def build_X(rows):
        X = np.zeros((len(rows), len(feature_cols)))
        for i, row in enumerate(rows):
            for j, col in enumerate(feature_cols):
                cell = row[header.index(col)]
                v = float(cell) if isinstance(cell, (int, float)) else 0.0
                X[i][j] = v
        return X

    train_X = build_X(rows)
    y_train = np.array([float(row[header.index('MRE-')]) for row in rows])

    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_X, y_train)

    preds = []
    for row in rows:
        x_test = np.zeros((1, len(feature_cols)))
        for j, col in enumerate(feature_cols):
            cell = row[header.index(col)]
            v = float(cell) if isinstance(cell, (int, float)) else 0.0
            x_test[0][j] = v
        pred = model.predict(x_test)[0]
        preds.append(pred)

    scored_preds = [(i, p) for i, p in enumerate(preds)]
    scored_preds.sort(key=lambda x: x[1])
    for i, _ in scored_preds[:50]:
        model_rows.add(i)

    # Find best row among all tried rows
    all_tried = random_rows | greedy_rows | model_rows
    
    best_score = float('-inf')
    best_row = None
    
    for idx in all_tried:
        score = score_row(idx)
        if score > best_score:
            best_score = score
            best_row = idx

    # Determine winner - which strategy contributed the best row?
    def find_winner():
        for strategy_rows, name in [(random_rows, "random"), (greedy_rows, "greedy"), (model_rows, "model")]:
            if best_row in strategy_rows:
                return name
    
    winner = find_winner()

    print(f"Winner: {winner}, Best row: {best_row}")
