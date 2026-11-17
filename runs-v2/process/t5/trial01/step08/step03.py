#!/usr/bin/env python3 -B
"""step03.py: test whether small-team setups really cost less."""
import ezr


def certify(xs, ys):
    """Return True if xs and ys are essentially the same (apart from noise), False otherwise."""
    return ezr.same(xs, ys)


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]

    header = [s for s in lines[0].split(",")]
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    team_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")

    # Split teams by median of Team Size
    team_vals = [r[team_idx] for r in rows]
    team_vals.sort()
    med = team_vals[len(team_vals) // 2]

    small_cost = []
    big_cost = []
    for row in rows:
        if row[team_idx] <= med:
            small_cost.append(row[cost_idx])
        else:
            big_cost.append(row[cost_idx])

    same = certify(small_cost, big_cost)

    print(f"Small-team Cost- vs Big-team Cost-: {'same' if same else 'different'}")
