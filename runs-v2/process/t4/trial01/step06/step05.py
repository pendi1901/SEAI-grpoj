import sys
sys.path.insert(0, '.')
from step01 import remember


def blame(header, rows):
    goal_cols = [c for c in header if c.endswith('-')]

    n = len(rows)
    scores = np.zeros(n)
    for col in goal_cols:
        vals = np.array([float(r[header.index(col)]) for r in rows])
        sorted_idx = np.argsort(vals)
        ranks = np.zeros(n)
        ranks[sorted_idx] = np.arange(n, 0, -1) / n
        scores += ranks

    # Worst positions (highest combined score = worst performance)
    threshold = np.percentile(scores, 95)
    worst_positions = [i for i in range(n) if scores[i] >= threshold]

    input_cols = [c for c in header if not c.endswith('-')]

    results = []
    for col in input_cols:
        vals_worst = []
        vals_rest = []
        for i, r in enumerate(rows):
            val = float(r[col])
            if i in worst_positions:
                vals_worst.append(val)
            else:
                vals_rest.append(val)

        mean_w = np.mean(vals_worst) if vals_worst else 0.0
        mean_r = np.mean(vals_rest) if vals_rest else 0.0

        diff = abs(mean_w - mean_r)
        results.append((col, diff))

    results.sort(key=lambda x: -x[1])

    return [f"{c}: avg worst={m:.3f}, avg rest={r:.3f}" for c, (m, r) in zip([r[0] for r in results], results)]


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = [list(r) for _, r in df.iterrows()]

    answer = blame(header, rows)
    print("\n".join(answer))
