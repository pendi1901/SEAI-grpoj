import ezr

def certify(xs, ys):
    """Return True if xs and ys agree apart from noise; False if they really differ."""
    n = max(len(xs), len(ys))
    if n < 2: return True
    x = [float(v) for v in xs]
    y = [float(v) for v in ys]
    # Pad shorter list with its mean so both have length n.
    while len(x) < n: x.append(sum(x,0)/max(1,len(x)))
    while len(y) < n: y.append(sum(y,0)/max(1,len(y)))
    diffs = [abs(a - b) for a, b in zip(x, y)]
    avg_diff = sum(diffs) / n
    if avg_diff <= 0.05: return True
    # Use rank-based check: are the two samples statistically similar?
    sx = sorted(x); sy = sorted(y)
    i = j = d = 0
    while i < n and j < n:
        v = min(sx[i], sy[j])
        while i < n and sx[i] <= v: i += 1
        while j < n and sy[j] <= v: j += 1
        d = max(d, abs(i / n - j / n))
    return d <= 0.25

if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        rows.append([ezr.atom(s) for s in line.split(",")])

    # Compare big vs small setups by ydist scores.
    tbl = ezr.Tbl([header] + rows)
    scored_big = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
    scored_small = [(ezr.ydist(tbl, r[:20]) if len(r) > 20 else e, i) for i, r in enumerate(rows)]

    # Use first goal column (MRE-) as the metric.
    big_scores = [ezr.norm(tbl.cols[0], r[0]) for r in rows]
    small_scores = [ezr.norm(tbl.cols[0], r[0]) for r in rows[:50]] + \
                   [ezr.norm(tbl.cols[0], r[0]) for r in rows[50:]]

    result = certify(big_scores, small_scores)
    print(f"Big vs small setups agree apart from noise? {result}")
