import ezr


def guess(header, train, test):
    # Identify goal columns (names ending in + or -)
    goals = [c for c in header if c[-1] in "+-"]
    
    def predict_one(col_name, rows):
        """Simple linear regression from scratch using only built-in types."""
        n = len(rows)
        # Build feature matrix: all non-goal columns as inputs
        x_cols = [c for i, c in enumerate(header) if c not in goals and c[-1] != "X"]
        
        # For each goal column, fit a model using training rows where it's known
        # Then predict on test rows
        
        # Collect input features from all rows (both train and test)
        x_vals = []
        for row in rows:
            feats = [row[i] if isinstance(row[i], float) else 0.0 
                     for i in range(len(x_cols))]
            x_vals.append(feats)
        
        # For the target column, use training values where known
        y_known = []
        for row in rows:
            val = row[header.index(col_name)]
            if isinstance(val, float):
                y_known.append(val)
            else:
                y_known.append(None)
        
        # Simple OLS linear regression
        k = len(x_cols)
        # Build X'X and X'y matrices
        XtX = [[0.0]*k for _ in range(k)]
        Xty = [0.0] * k
        
        for i, feats in enumerate(x_vals):
            for j in range(k):
                XtX[j][j] += feats[j]**2 if isinstance(feats[j], float) else 1.0
            for j in range(k):
                Xty[j] += (feats[j] * y_known[i]) if isinstance(feats[j], float) and y_known[i] is not None else 0.0
        
        # Solve using Gaussian elimination with partial pivoting
        aug = [row[:] + [y_known[i]] for i, row in enumerate(x_vals)]
        
        for col in range(k):
            max_row = col
            for row in range(col+1, len(aug)):
                if abs(aug[row][col]) > abs(aug[max_row][col]):
                    max_row = row
            aug[col], aug[max_row] = aug[max_row], aug[col]
            
            pivot = aug[col][col]
            for row in range(col+1, len(aug)):
                factor = aug[row][col] / pivot if isinstance(pivot, float) and pivot != 0 else 0.0
                for j in range(k+1):
                    aug[row][j] -= factor * aug[col][j]
        
        # Back substitution
        coeffs = [0.0] * k
        for i in range(len(aug)-1, -1, -1):
            if abs(aug[i][i]) < 1e-32:
                coeffs[i] = 0.0
            else:
                s = aug[i][-1]
                for j in range(i+1, len(aug)):
                    s -= aug[i][j] * coeffs[j]
                coeffs[i] = s / aug[i][i]
        
        return coeffs
    
    # For each goal column, fit model on train data, predict test
    predictions = []
    for col_name in goals:
        coeffs = predict_one(col_name, train)
        # Predict for test rows
        x_cols = [c for i, c in enumerate(header) if c not in goals and c[-1] != "X"]
        for row in test:
            feats = [row[i] if isinstance(row[i], float) else 0.0 
                     for i in range(len(x_cols))]
            pred = sum(coeffs[j] * feats[j] for j in range(len(feats)))
            predictions.append(pred)
    
    return predictions


if __name__ == "__main__":
    with open("Health-ClosedIssues0000.train.csv", encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]
    header = list(lines[0].split(","))
    rows   = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    
    train_rows = []
    test_rows  = []
    # Split: first part is train, rest is test (but we need to know the split)
    # Since the customer says "Any count the customer quotes describes their full records"
    # and doesn't specify a split, use all rows as train for now
    # Actually, let's just use all available data
    
    predictions = guess(header, rows, [])
    
    print(f"Predicted {len(predictions)} goal values using linear regression on input features.")
