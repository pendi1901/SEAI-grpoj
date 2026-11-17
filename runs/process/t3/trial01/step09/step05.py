import numpy as np


def blame(header, rows):
    goal_cols = [c for c in header if c.endswith('-')]
    
    def parse_row(row_dict):
        vals = {}
        for col in header:
            v = row_dict[header.index(col)]
            try:
                vals[col] = float(v)
            except (ValueError, TypeError):
                vals[col] = np.nan
        return vals
    
    parsed = [parse_row(r) for r in rows]
    
    idle_col = 'Idle-'
    idle_vals = []
    for p in parsed:
        v = p[idle_col]
        if not np.isnan(v):
            idle_vals.append(v)
    
    n = len(rows)
    worst_idx = int(0.1 * n)
    sorted_by_idle = np.argsort(idle_vals)[::-1][:worst_idx].tolist()
    
    input_cols = [c for c in header if not c.endswith('-')]
    
    correlations = []
    for col in input_cols:
        vals = []
        for i, p in enumerate(parsed):
            v = p[col]
            if np.isnan(v) or not np.isfinite(v):
                continue
            vals.append((v, idle_vals[i]))
        
        if len(vals) < 3:
            correlations.append(0.0)
            continue
        
        xs = [x for x, _ in vals]
        ys = [y for _, y in vals]
        
        mean_x = np.mean(xs)
        mean_y = np.mean(ys)
        std_x = float(np.std(xs))
        std_y = float(np.std(ys))
        
        if std_x < 1e-9 or std_y < 1e-9:
            correlations.append(0.0)
            continue
        
        corr = np.sum((np.array(xs) - mean_x) * (np.array(ys) - mean_y)) / (std_x * std_y)
        correlations.append(float(corr))
    
    ranked = sorted(range(len(correlations)), key=lambda i: correlations[i], reverse=True)
    
    result = []
    for rank in ranked[:5]:
        col = input_cols[rank]
        if abs(correlations[rank]) > 0.1:
            result.append(col)
    
    return result


if __name__ == "__main__":
    import pandas as pd
    
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]
    
    blame_result = blame(header, rows)
    print(f"Inputs explaining high Idle-: {blame_result}")
