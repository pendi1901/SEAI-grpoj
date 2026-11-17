import random
from step07 import choose as choose_random


def race(header, rows, label):
    """Compare three strategies on up to 50 trials; return a dict."""
    goals = [c for c in header if c.endswith('-') and c[0].isupper()]

    def score(row):
        return sum(float(row[header.index(g)]) for g in goals)

    # --- Strategy 1: random (already defined in step07) ---
    trials_random = set(random.sample(range(len(rows)), min(50, len(rows))))
    best_pos_r = None
    best_score_r = float('inf')
    for i in trials_random:
        s = score(label(i))
        if s < best_score_r:
            best_score_r = s
            best_pos_r = i

    # --- Strategy 2: remember (from step01) ---
    from step01 import remember as remember_rows
    n = len(rows)
    scored_all = [(sum(float(row[header.index(g)]) for g in goals), i)
                   for i, row in enumerate(rows)]
    scored_all.sort()
    k = max(1, int(n * 0.05))
    top_indices = [pos for _, pos in scored_all[:k]]

    # Pick the best among those top indices (greedy pick).
    best_pos_g = None
    best_score_g = float('inf')
    for i in top_indices:
        s = score(label(i))
        if s < best_score_g:
            best_score_g = s
            best_pos_g = i

    # --- Strategy 3: spot (from step09) — pick the least suspicious row ---
    from step09 import spot as spot_rows
    suspicious = spot(header, rows)
    if not suspicious:
        suspicious = set()
    else:
        suspicious = set(suspicious)

    # Try all non-suspicious rows.
    best_pos_s = None
    best_score_s = float('inf')
    for i in range(n):
        if i in suspicious:
            continue
        s = score(label(i))
        if s < best_score_s:
            best_score_s = s
            best_pos_s = i

    # Determine the winner.
    scores = {
        "random": (best_score_r, best_pos_r),
        "greedy": (best_score_g, best_pos_g),
        "spot":   (best_score_s, best_pos_s),
    }
    winner_name = min(scores, key=lambda k: scores[k][0])

    return {
        "winner": winner_name,
        "row": scores[winner_name][1],
        "tried": ["random", "greedy", "spot"],
    }


if __name__ == "__main__":
    import csv
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [list(map(float, r)) for r in reader]

    result = race(header, rows, lambda i: list(map(float, rows[i])))
    print(f"Winner: {result['winner']}")
    print(f"Best row position: {result['row']}")
    print(f"All tried: {result['tried']}")
