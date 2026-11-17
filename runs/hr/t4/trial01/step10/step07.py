import pandas as pd


def choose(header, rows, label):
    """Pick up to 50 employees and return the position of the one with the best goals."""
    
    # Goals are '+' columns (YearsAtCompany+, YearsInCurrentRole+)
    goals_plus = [h for h in header if h.endswith('+')]
    
    # We don't know any row's goals initially, so pick 50 rows to interview.
    n_rows = len(rows)
    sample_size = min(50, n_rows)
    
    best_idx = None
    best_score = -float('inf')
    
    for i in range(sample_size):
        true_goals = label(i)
        
        # Score: sum of normalized '+' goals (higher is better)
        s = 0.0
        for c in goals_plus:
            v = float(true_goals[c])
            lo, hi = -float('inf'), float('inf')
            rng = (hi - lo) or 1.0
            s += (v - lo) / rng
        
        if s > best_score:
            best_score = s
            best_idx = i
    
    return best_idx


if __name__ == "__main__":
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    # Replace goal cells with "?" to simulate the hidden scenario
    goals_plus = [h for h in header if h.endswith('+')]
    for i, row in enumerate(rows):
        for c in goals_plus:
            row[c] = "?"

    best_pos = choose(header, rows, lambda i: df.iloc[i][goals_plus].tolist())
    
    print(f"Best employee to interview is at position {best_pos}.")
    print(f"YearsAtCompany+={df.iloc[best_pos]['YearsAtCompany+']}, "
          f"YearsInCurrentRole+={df.iloc[best_pos]['YearsInCurrentRole+']}")
