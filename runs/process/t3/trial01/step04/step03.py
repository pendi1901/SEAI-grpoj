import numpy as np


def certify(xs, ys):
    """Returns True if xs and ys are the same apart from noise."""
    arr_x = np.array(xs)
    arr_y = np.array(ys)
    
    mean_diff = abs(np.mean(arr_x) - np.mean(arr_y))
    std_x = float(np.std(arr_x))
    std_y = float(np.std(arr_y))
    combined_std = np.sqrt(std_x**2 + std_y**2) if (std_x > 0 or std_y > 0) else 1.0
    
    return mean_diff < 2 * combined_std


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    team_size_col = 'Team Size'
    cost_col = 'Cost-'

    ts_vals = []
    costs = []
    for row in rows:
        v = row[header.index(team_size_col)]
        if v == '?':
            continue
        ts_vals.append(float(v))
        c = float(row[header.index(cost_col)])
        costs.append(c)

    median_ts = np.median(ts_vals)
    
    small_cost = [c for t, c in zip(ts_vals, costs) if t <= median_ts]
    big_cost = [c for t, c in zip(ts_vals, costs) if t > median_ts]

    result = certify(small_cost, big_cost)
    print(
        f"Small-team Cost- vs Big-team Cost-: "
        f"{'same apart from noise' if result else 'really different'}"
    )
