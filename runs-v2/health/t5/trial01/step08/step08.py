import ezr


def fix(header, row, levers):
    """Find lever values that would improve this bad row."""
    
    tbl = ezr.Tbl([header] + [row])
    
    def ydist_row(r):
        return ezr.ydist(tbl, r)
    
    # Start with the original row as a candidate.
    candidates = [dict(zip(header, row))]
    
    for col_name, allowed in levers.items():
        new_candidates = []
        for cand in candidates:
            if isinstance(allowed, tuple) and len(allowed) == 2:
                lo, hi = allowed
                vals = [lo, hi, (lo + hi) / 2]
            else:
                vals = list(allowed)
            
            for val in vals:
                new_row = cand[:]
                new_row[header.index(col_name)] = val
                new_candidates.append(dict(zip(header, new_row)))
        
        candidates = new_candidates
    
    best_combo = {}
    best_ydist = 1e30
    
    for cand in candidates:
        yd = ydist_row(cand)
        if yd < best_ydist:
            best_ydist = yd
            best_combo = {k: v for k, v in zip(header, cand)}
    
    return best_combo


if __name__ == "__main__":
    csv_path = "Health-ClosedIssues0000.train.csv"
    with open(csv_path, encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    header = list(lines[0].split(","))
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    
    tbl = ezr.Tbl(rows)
    
    def ydist_row(r):
        return ezr.ydist(tbl, r)
    
    worst_idx = min(range(len(rows)), key=lambda i: ydist_row(rows[i]))
    worst_row = rows[worst_idx]
    
    levers = {
        "N_estimators": (10, 200),
        "Min_sample_leaves": (3, 50),
        "Max_depth": (8, 20),
        "criterion": ["squared_error", "absolute_error"],
        "Min_impurity_decrease": (0.0, 10.0),
    }
    
    result = fix(header, worst_row, levers)
    print(f"Row {worst_idx} ydist={ydist_row(worst_row):.4f} -> improved to {ezr.ydist(tbl, [header] + [result]):.4f}")
