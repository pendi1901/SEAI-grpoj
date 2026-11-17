import csv


def certify(xs, ys):
    """Return True if xs and ys agree apart from noise, False if they really differ."""
    mx = max(len(xs), len(ys))
    if mx == 0:
        return True
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    diff = abs(mean_x - mean_y)
    # Use the larger sample's std as a noise proxy.
    n1, n2 = len(xs), len(ys)
    if n1 > 0:
        var_x = sum((v - mean_x) ** 2 for v in xs) / (n1 - 1) if n1 > 1 else 0.0
        s_x = var_x ** 0.5
    else:
        s_x = 0.0
    if n2 > 0:
        var_y = sum((v - mean_y) ** 2 for v in ys) / (n2 - 1) if n2 > 1 else 0.0
        s_y = var_y ** 0.5
    else:
        s_y = 0.0
    noise = ((s_x ** 2 + s_y ** 2) ** 0.5) * (n1 ** -0.5 + n2 ** -0.5)
    return diff < 3.0 * noise


def certify(xs, ys):
    """Return True if xs and ys agree apart from noise, False if they really differ."""
    mx = max(len(xs), len(ys))
    if mx == 0:
        return True
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    diff = abs(mean_x - mean_y)
    n1, n2 = len(xs), len(ys)
    s_x = (sum((v - mean_x) ** 2 for v in xs) / max(n1 - 1, 1)) ** 0.5 if n1 > 1 else 0.0
    s_y = (sum((v - mean_y) ** 2 for v in ys) / max(n2 - 1, 1)) ** 0.5 if n2 > 1 else 0.0
    noise = ((s_x ** 2 + s_y ** 2) ** 0.5) * (n1 ** -0.5 + n2 ** -0.5)
    return diff < 3.0 * noise


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [list(map(float, row)) for row in reader]

    # Small-team vs big-team on Cost- (lower is better).
    median_ts = sorted([rows[i][header.index('Team Size')] for i in range(len(rows))])[len(rows) // 2]
    small_cost = [rows[i][header.index('Cost-')] for i in range(len(rows)) if rows[i][header.index('Team Size')] <= median_ts]
    big_cost = [rows[i][header.index('Cost-')] for i in range(len(rows)) if rows[i][header.index('Team Size')] > median_ts]

    print(f"Small-team mean Cost-: {sum(small_cost)/len(small_cost):.4f}  (n={len(small_cost)})")
    print(f"Big-team   mean Cost-: {sum(big_cost)/len(big_cost):.4f}  (n={len(big_cost)})")
    if certify(small_cost, big_cost):
        print("Verdict: the difference is just noise — small teams were not really cheaper.")
    else:
        print("Verdict: the difference is real — small-team setups are genuinely cheaper than big-team ones.")
