import ezr


def race(header, rows, label):
    """Three strategies compete; return winner dict."""

    def ydist_row(tbl, row):
        return ezr.ydist(tbl, list(row))

    # ---- Strategy 1: random (must be one) -------------------------------
    def _random():
        n = len(rows)
        chosen = set()
        while len(chosen) < 50 and len(rows) > 0:
            i = int(random.random() * len(rows))
            chosen.add(i)
        tbl = ezr.Tbl([header] + [list(r) for r in rows])
        scored = [(ydist_row(tbl, list(rows[i])), i) for i in chosen]
        scored.sort(key=lambda x: x[0])
        return scored[0][1], "random"

    # ---- Strategy 2: acquire (ezr's smart label-budgeted search) ---------
    def _acquire():
        tbl = ezr.Tbl([header] + [list(r) for r in rows])
        chosen = ezr.acquire(tbl, cap=50, label=label)
        scored = [(ydist_row(tbl, list(r)), i) for i, r in enumerate(chosen)]
        scored.sort(key=lambda x: x[0])
        return scored[0][1], "acquire"

    # ---- Strategy 3: grabs (ezr's random label-budgeted search) ---------
    def _grabs():
        tbl = ezr.Tbl([header] + [list(r) for r in rows])
        chosen = ezr.grabs(tbl, cap=50, label=label)
        scored = [(ydist_row(tbl, list(r)), i) for i, r in enumerate(chosen)]
        scored.sort(key=lambda x: x[0])
        return scored[0][1], "grabs"

    # ---- Run all three --------------------------------------------------
    a1 = _random()
    a2 = _acquire()
    a3 = _grabs()

    best_y = min(a1[0], a2[0], a3[0])
    winner_name = [s for s, y in [(a1[1], a1[0]), (a2[1], a2[0]), (a3[1], a3[0])] if y == best_y][0]

    return {"winner": winner_name, "row": best_y, "tried": ["random", "acquire", "grabs"]}


if __name__ == "__main__":
    import os
    path = 'pom3a.train.csv'
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(',')
    rows = ezr.csv(path)

    # label(i) reveals true goal values for row i (all goals are minimised, goal=1)
    def label(i):
        return [float(row[c.at]) for row in rows[i:i+1] for c in ezr.Tbl([header] + [list(rows[i:i+1])]).y if c.goal == 1 and type(c) is ezr.Num]

    result = race(header, rows, label)
    print(f"Winner: {result['winner']} found row {result['row']}")
