import ezr

def blame(header, rows):
    tbl = ezr.Tbl([header] + [list(r) for r in rows])

    # Build a tree on all data; ranker scores each row by its leaf's mean ydist
    rank_fn = ezr.ranker(tbl)

    scored = [(rank_fn(r), i, list(r)) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: -x[0])  # worst first

    n = len(rows)
    worst_n = max(1, int(n * 0.05))
    best_n = max(1, int(n * 0.05))

    worst_rows = [r for _, _, r in scored[:worst_n]]
    best_rows = [r for _, _, r in scored[-best_n:]]

    # For each input column, measure how much it differs between worst and best rows
    blame_scores = []
    for col in tbl.x:
        if type(col) is ezr.Num:
            w_vals = [r[col.at] for r in worst_rows if r[col.at] != "?"]
            b_vals = [r[col.at] for r in best_rows if r[col.at] != "?"]
            if not w_vals or not b_vals: continue
            w_mean = sum(w_vals) / len(w_vals)
            b_mean = sum(b_vals) / len(b_vals)
            blame_scores.append((abs(b_mean - w_mean), col.txt))
        else:  # Sym
            w_set = set(r[col.at] for r in worst_rows if r[col.at] != "?")
            b_set = set(r[col.at] for r in best_rows if r[col.at] != "?")
            if not w_set or not b_set: continue
            blame_scores.append((abs(len(w_set) - len(b_set)), col.txt))

    blame_scores.sort(key=lambda x: -x[0])

    # Return the input column names that explain the worst rows, ordered by importance
    return [name for _, name in blame_scores if name]


if __name__ == "__main__":
    import os
    path = 'pom3a.train.csv'
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(',')
    rows = ezr.csv(path)

    result = blame(header, rows)
    print(f"Worst setups are bad because of: {', '.join(result)}")
