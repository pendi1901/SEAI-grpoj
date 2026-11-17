import ezr

def spot(header, rows):
    """Find rows that look like failed runs."""
    tbl = ezr.Tbl([header] + rows)
    scored = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: -x[0])  # highest ydist first (worst)
    
    n = len(scored)
    if n < 3: return []
    
    med = sorted(x[0] for x in scored)[n // 2]
    worst = [i for _, i in scored[:max(1, int(n * 0.05))]]
    
    # Also flag rows with suspicious parameter ranges (e.g., zero estimators)
    suspicious_params = {
        "N_estimators": lambda v: isinstance(v, (int, float)) and v <= 0,
        "Max_depth": lambda v: isinstance(v, (int, float)) and v < 1,
        "Min_sample_leaves": lambda v: isinstance(v, (int, float)) and v <= 0,
    }
    
    bad_params = []
    for i, row in enumerate(rows):
        for col_name, check_fn in suspicious_params.items():
            if col_name in header:
                idx = header.index(col_name)
                val = row[idx]
                if isinstance(val, (int, float)) and check_fn(val):
                    bad_params.append(i)
    
    all_bad = sorted(set(worst + bad_params), reverse=True)
    return all_bad[:20]

if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        rows.append([ezr.atom(s) for s in line.split(",")])

    bad = spot(header, rows)
    print(f"Suspected failed runs (positions): {bad}")
