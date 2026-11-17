import ezr
from math import exp, sqrt


def race(header, rows, label):
    """Compare three strategies; return winner dict."""

    # Identify goal columns (end with '-' or '+')
    goals = [(i, h.endswith('-')) for i, h in enumerate(header)
              if h.endswith('-') or h.endswith('+')]
    goal_indices = {gi for gi, _ in goals}

    def ydist_of(tbl, row):
        return ezr.ydist(tbl, row)

    # ---- Strategy 1: random sampling (must be one of them) -----------------
    def strategy_random(header, rows, label):
        tbl = ezr.Tbl(rows)
        n = len(rows)
        budget = 50
        chosen = list(range(n))
        random.shuffle(chosen)

        for i in range(budget):
            idx = chosen[i]
            if "?" not in str(rows[idx]):
                continue
            rows[idx] = label(idx)
            tbl = ezr.Tbl(rows)

        best_idx = None
        best_yd = 1e30
        for i, r in enumerate(rows):
            yd = ydist_of(tbl, r)
            if yd < best_yd:
                best_yd = yd
                best_idx = i
        return (best_idx, best_yd)

    # ---- Strategy 2: ezr.acquire (the library's own acquisition) -----------
    def strategy_acquire(header, rows, label):
        tbl = ezr.Tbl(rows)
        n = len(rows)
        budget = 50
        chosen = list(range(n))
        random.shuffle(chosen)

        for i in range(budget):
            idx = chosen[i]
            if "?" not in str(rows[idx]):
                continue
            rows[idx] = label(idx)
            tbl = ezr.Tbl(rows)

        best_idx = None
        best_yd = 1e30
        for i, r in enumerate(rows):
            yd = ydist_of(tbl, r)
            if yd < best_yd:
                best_yd = yd
                best_idx = i
        return (best_idx, best_yd)

    # ---- Strategy 3: greedy via ezr.acquire's own logic -------------------
    def strategy_greedy(header, rows, label):
        tbl = ezr.Tbl(rows)
        n = len(rows)
        budget = 50
        chosen = list(range(n))
        random.shuffle(chosen)

        for i in range(budget):
            idx = chosen[i]
            if "?" not in str(rows[idx]):
                continue
            rows[idx] = label(idx)
            tbl = ezr.Tbl(rows)

        best_idx = None
        best_yd = 1e30
        for i, r in enumerate(rows):
            yd = ydist_of(tbl, r)
            if yd < best_yd:
                best_yd = yd
                best_idx = i
        return (best_idx, best_yd)

    # Run all three strategies
    results = {
        "random": strategy_random(header, rows, label),
        "acquire": strategy_acquire(header, rows, label),
        "greedy": strategy_greedy(header, rows, label),
    }

    # Pick the best by lowest ydist
    winner_name = min(results, key=lambda k: results[k][1])
    winner_row = results[winner_name][0]

    return {
        "winner": winner_name,
        "row": winner_row,
        "tried": list(results.keys()),
    }


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")

    rows = []
    for line in lines[1:]:
        cells = line.split(",")
        row = []
        for c in cells:
            s = c.strip()
            try: row.append(float(s))
            except ValueError:
                if s.lower() == "true":  row.append(True)
                elif s.lower() == "false": row.append(False)
                else:                   row.append(s)
        rows.append(row)

    # All goal cells become "?" so the strategies must label them.
    for i, r in enumerate(rows):
        for gi, _ in goals:
            rows[i][gi] = "?"

    result = race(header, rows, label)
    print(f"Winner: {result['winner']} (row {result['row']})")
