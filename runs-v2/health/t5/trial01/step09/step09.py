import ezr


def spot(header, rows):
    """Find rows whose input cells look wrongly entered."""
    # Identify numeric input columns (uppercase, no +/-) and symbolic ones.
    goals = [c for c in header if c[-1] in "+-"]
    inputs = [c for i, c in enumerate(header) if c not in goals and c[-1] != "X"]

    tbl = ezr.Tbl(rows)

    # For each numeric input column, compute mean & std via Welford.
    col_stats = {}  # at -> (mean, sd, n)
    for i, name in enumerate(header):
        if not name[0].isupper() or name[-1] in "+-":
            continue
        col_stats[i] = ezr.add(ezr.Num(name=name, at=i), rows[i][i])

    # Now scan each row: flag any cell that is a statistical outlier.
    suspicious = []
    for i, row in enumerate(rows):
        worst_z = 0.0
        for j, name in enumerate(header):
            if not name[0].isupper() or name[-1] in "+-":
                continue
            at = ezr.add(ezr.Num(name=name, at=j), row[j])
            # Reuse stats: compute z-score against column distribution.
        # Simpler: just check each numeric input cell for extreme values.
    # Let me redo this cleanly.

    # Compute per-column mean and std once using ezr's add (Welford).
    col_mu = {}
    col_m2 = {}
    col_n = {}
    for i, name in enumerate(header):
        if not name[0].isupper() or name[-1] in "+-":
            continue
        n = 0; mu = 0.0; m2 = 0.0
        for row in rows:
            v = row[i]
            n += 1
            d = v - mu
            mu += d / n
            m2 += (v - mu) * (v - mu)
        sd = (m2 / max(1, n - 1)) ** 0.5 if n >= 2 else 0.0
        col_mu[i] = mu
        col_m2[i] = m2
        col_n[i] = n

    suspicious = []
    for i, row in enumerate(rows):
        worst_z = 0.0
        for j, name in enumerate(header):
            if not name[0].isupper() or name[-1] in "+-":
                continue
            v = row[j]
            mu = col_mu[j]
            sd = (col_m2[j] / max(1, col_n[j] - 1)) ** 0.5 if col_n[j] >= 2 else 0.0
            if sd < 1e-32:
                continue
            z = abs(v - mu) / sd
            if z > worst_z:
                worst_z = z
        if worst_z > 3.0:
            suspicious.append((i, worst_z))

    # Sort by how extreme the outlier is (most suspicious first).
    suspicious.sort(key=lambda x: -x[1])
    return [idx for idx, _ in suspicious]


if __name__ == "__main__":
    with open("Health-ClosedIssues0000.train.csv", encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]
    header = list(lines[0].split(","))
    rows   = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    bad = spot(header, rows)
    print(f"Suspect rows (most suspicious first): {bad}")
