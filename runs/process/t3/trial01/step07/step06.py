import numpy as np


def justify(header, rows, row):
    goal_cols = [c for c in header if c.endswith('-')] or \
                [c for c in header if c.endswith('+')]
    
    input_cols = [c for c in header if not c.endswith('-') and not c.endswith('+')]

    def parse_row(row_dict, cols):
        vals = []
        for col in cols:
            v = row_dict[header.index(col)]
            try:
                vals.append(float(v))
            except (ValueError, TypeError):
                return None
        return np.array(vals)

    # Build training data from rows where goals are not "?"
    train_rows = []
    for r in rows:
        if any(r[header.index(c)] == '?' for c in goal_cols):
            continue
        parsed = parse_row(r, input_cols)
        if parsed is None:
            continue
        train_rows.append(parsed)

    # Predict each goal column using linear regression on training data
    predictions = {}
    for col in goal_cols:
        y_vals = []
        X_train = np.array(train_rows)
        for r in rows:
            if any(r[header.index(c)] == '?' for c in goal_cols):
                continue
            parsed = parse_row(r, input_cols)
            if parsed is None:
                continue
            v = float(r[header.index(col)])
            y_vals.append(v)

        X_train = np.array(train_rows)
        y_train = np.array(y_vals)
        
        valid_mask = ~np.isnan(X_train).any(axis=1) & ~np.isnan(y_train)
        if valid_mask.sum() < 2:
            predictions[col] = None
            continue
        
        model = LinearRegression()
        model.fit(X_train[valid_mask], y_train[valid_mask])

        test_inputs = parse_row(row, input_cols)
        if test_inputs is None:
            return (0.0, "Cannot predict goals for this setup")
        
        pred = float(model.predict([test_inputs])[0])
        predictions[col] = pred

    # Compare predicted row against each complete row
    n = len(rows)
    better_count = 0
    
    for r in rows:
        if any(r[header.index(c)] == '?' for c in goal_cols):
            continue
        
        parsed = parse_row(r, input_cols)
        if parsed is None:
            continue
        
        our_preds = {col: predictions[col] for col in goal_cols}
        
        # Check if every goal of the complete row is worse than ours
        all_worse = True
        for col in goal_cols:
            other_val = float(r[header.index(col)])
            our_val = our_preds[col]
            
            if col.endswith('-'):
                # Lower is better; other must be strictly higher to count as "worse"
                if not (other_val > our_val):
                    all_worse = False
            elif col.endswith('+'):
                # Higher is better; other must be strictly lower to count as "worse"
                if not (other_val < our_val):
                    all_worse = False
        
        if all_worse:
            better_count += 1

    p = better_count / n if n > 0 else 0.0
    
    reason_parts = []
    for col in goal_cols:
        other_vals = [float(r[header.index(col)]) for r in rows 
                      if any(r[header.index(c)] == '?' for c in goal_cols) or True]
    
    avg_pred = {col: predictions[col] for col in goal_cols}
    reason_parts.append(f"predicted {', '.join(f'{c}: {avg_pred[c]:.2f}' for c in goal_cols)}")

    return (p, f"{better_count}/{n} setups are worse than this one ({reason_parts[0]})")


if __name__ == "__main__":
    import pandas as pd
    
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    # Find a test row (one with "?" goals)
    test_row = None
    for r in rows:
        if any(r[header.index(c)] == '?' for c in header if c.endswith('-')):
            test_row = r
            break
    
    p, reason = justify(header, rows, test_row)
    print(f"This setup beats {p:.1%} of all setups. Reason: {reason}")
