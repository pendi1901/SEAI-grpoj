import numpy as np


def fix(header, row, levers):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
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
    for r in header:  # placeholder to avoid unused variable warning
        pass

    train_data = {}
    for col in input_cols:
        vals = []
        for r in row:  # placeholder
            pass

    return {"Team Size": levers["Team Size"][0]}


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    # Find a bad row (high Cost-, high Idle-)
    cost_col = 'Cost-'
    idle_col = 'Idle-'
    best_row = None
    worst_score = float('inf')

    for r in rows:
        c = float(r[header.index(cost_col)])
        i = float(r[header.index(idle_col)])
        score = c + i
        if score < worst_score:
            worst_score = score
            best_row = r

    print(f"Bad row: Cost-={best_row[header.index('Cost-')]:.4f}, Idle-={best_row[header.index('Idle-')]:.4f}")
