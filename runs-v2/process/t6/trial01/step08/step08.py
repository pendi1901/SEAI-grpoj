import ezr

def fix(header, row, levers):
    tbl = ezr.Tbl([header] + [list(row)])
    rank_fn = ezr.ranker(tbl)
    cur_y = rank_fn(list(row))

    best_col = None
    best_val = None
    best_improvement = 0

    for col_name, vals in levers.items():
        for v in vals:
            new_row = list(row)
            idx = header.index(col_name)
            if type(v) is str:
                new_row[idx] = v
            else:
                new_row[idx] = float(v)

            tbl2 = ezr.Tbl([header] + [new_row])
            rank_fn2 = ezr.ranker(tbl2)
            y = rank_fn2(new_row)
            improvement = cur_y - y

            if improvement > best_improvement:
                best_improvement = improvement
                best_col = col_name
                best_val = v

    return {best_col: best_val}


if __name__ == "__main__":
    import os
    path = 'pom3a.train.csv'
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(',')
    rows = ezr.csv(path)

    tbl_full = ezr.Tbl([header] + list(rows))
    rank_fn = ezr.ranker(tbl_full)
    scored = [(rank_fn(list(r)), i) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: -x[0])

    bad_row = rows[scored[0][1]]
    levers = {col.txt: [f"{col.mu:.2f}", f"{col.mu + col.sd:.2f}"]
              for col in tbl_full.x if type(col) is ezr.Num}

    result = fix(header, bad_row, levers)
    print(f"Fix: change {list(result.keys())[0]} to {result[list(result.keys())[0]]}")
