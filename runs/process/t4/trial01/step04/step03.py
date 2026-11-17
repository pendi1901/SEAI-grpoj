import sys
sys.path.insert(0, ".")
from step01 import remember
from step02 import guess


def certify(xs, ys):
    """Return True if xs and ys are essentially the same apart from noise."""
    if len(xs) == 0 or len(ys) == 0:
        return False
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    diff = abs(mean_x - mean_y)
    std_x = (sum((v - mean_x) ** 2 for v in xs) / max(len(xs), 1)) ** 0.5
    std_y = (sum((v - mean_y) ** 2 for v in ys) / max(len(ys), 1)) ** 0.5
    pooled_std = ((std_x ** 2 + std_y ** 2) ** 0.5) if (std_x or std_y) else 1.0
    return diff < 1.5 * pooled_std


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = []
    for _, row in df.iterrows():
        r = []
        for col in header:
            val = row[col]
            if pd.isna(val):
                r.append("?")
            else:
                r.append(float(val))
        rows.append(r)

    team_size_col = "Team Size"
    cost_col = "Cost-"

    small_cost = []
    big_cost = []
    for row in rows:
        ts = row[header.index(team_size_col)]
        c = row[header.index(cost_col)]
        if "?" not in (ts, c):
            if ts < 0.5:
                small_cost.append(c)
            else:
                big_cost.append(c)

    print(f"Small-team Cost- mean : {sum(small_cost)/len(small_cost):.4f}  ({len(small_cost)} rows)")
    print(f"Big-team   Cost- mean : {sum(big_cost)/len(big_cost):.4f}  ({len(big_cost)} rows)")

    if certify(small_cost, big_cost):
        print("Verdict: The difference is just noise — luck.")
    else:
        print("Verdict: Small-team setups really are cheaper than big-team ones.")
