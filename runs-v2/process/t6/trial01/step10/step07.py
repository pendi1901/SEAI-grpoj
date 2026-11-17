import ezr

def choose(header, rows, label):
    """Trial up to 50 setups; return the index of the best one."""
    # Pick diverse candidates by sampling across the data space.
    n = len(rows)
    if n <= 50:
        todo = list(range(n))
    else:
        step = max(1, int(n / 50))
        todo = [i for i in range(step - 1, n, step)]

    # Label each candidate and track its ydist using the revealed goals.
    best_idx = None
    best_y = float('inf')
    labeled = set()

    for i in todo:
        if i in labeled:
            continue
        labels = label(i)  # list of true goal values for row i
        labeled.add(i)

        # Compute ydist manually from the revealed goals.
        # Goal columns are those whose name ends with '-'.
        tbl = ezr.Tbl([header] + [list(r) for r in rows])
        ydist_val = 0.0
        cnt = 0
        for col in tbl.y:
            if col.goal != 0 and type(col) is ezr.Num:
                # labels[col.at] gives the true value; goal is 1 (minimize).
                val = float(labels[col.at])
                ydist_val += abs(val - col.goal) ** 2
                cnt += 1

        if cnt > 0:
            ydist_val = ydist_val ** 0.5 / (cnt ** 0.5)

        if ydist_val < best_y:
            best_y = ydist_val
            best_idx = i

    return best_idx


if __name__ == "__main__":
    import os
    path = 'pom3a.train.csv'
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(',')
    rows = ezr.csv(path)

    def label(i):
        """Reveal the true goal values for row i."""
        return [float(row[9]) for row in rows[i:i+1]]  # Cost- is column index 9

    idx = choose(header, rows, label)
    print(f"Best of up to 50 trials: setup {idx}")
