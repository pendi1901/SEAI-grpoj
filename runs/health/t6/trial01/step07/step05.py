import ezr


def blame(header, rows):
    """Return input column names that best explain why the worst rows are bad."""
    tbl = ezr.Tbl([header] + rows)

    scored = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: -x[0])  # worst first

    n_bad = max(1, int(len(scored) * 0.1))
    bad_idx = [i for _, i in scored[:n_bad]]
    good_idx = [i for i in range(len(rows)) if i not in bad_idx]

    bad_rows = [rows[i] for i in bad_idx]
    good_rows = [rows[i] for i in good_idx]

    blame_cols = []
    for col in tbl.x:
        bad_vals = [r[col.at] for r in bad_rows if r[col.at] != "?"]
        good_vals = [r[col.at] for r in good_rows if r[col.at] != "?"]
        if not bad_vals or not good_vals:
            continue

        if type(col) is ezr.Num:
            b_mean = sum(bad_vals) / len(bad_vals)
            g_mean = sum(good_vals) / len(good_vals)
            diff = abs(b_mean - g_mean)
            all_v = bad_vals + good_vals
            mu = sum(all_v) / len(all_v)
            m2 = sum((v - mu) ** 2 for v in all_v)
            sd = (m2 / max(1, len(all_v) - 1)) ** 0.5 if len(all_v) >= 2 else 1
            norm_diff = diff / sd if sd > 0 else 0
        elif type(col) is ezr.Sym:
            g_set = set(good_vals)
            bad_dist = sum(1 for v in bad_vals if v not in g_set)
            norm_diff = bad_dist / len(bad_vals) if bad_vals else 0
        else:
            continue

        blame_cols.append((norm_diff, col.txt))

    blame_cols.sort(key=lambda x: -x[0])
    return [c[1] for c in blame_cols[:5]]


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__), "Health-ClosedIssues0000.train.csv")
    rows = list(ezr.csv(path))
    header = rows[0]
    data_rows = rows[1:]

    result = blame(header, data_rows)
    print(f"Bad setups are damaged by: {', '.join(result)}")
