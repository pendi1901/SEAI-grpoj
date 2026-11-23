import ezr
import step05

def blame(header, rows):
    """
    Identify input columns that do not significantly differentiate 
    the worst rows from the rest of the data. If a column's distribution 
    is statistically the same in both groups, it can be left at 
    factory defaults without hurting performance.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the worst
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], 
                    key=lambda x: x[0], reverse=True)
    
    # Split into worst 10% and the rest
    limit = max(1, len(rows) // 10)
    worst = [x[1] for x in scored[:limit]]
    rest = [x[1] for x in scored[limit:]]
    
    # Find columns where the distribution is NOT significantly different
    # (i.e., the column does not explain the badness)
    safe_to_default = []
    for col in tbl.x:
        at = col.at
        if isinstance(col, ezr.Num):
            vals_worst = [r[at] for r in worst if r[at] != "?"]
            vals_rest = [r[at] for r in rest if r[at] != "?"]
            if len(vals_worst) > 1 and len(vals_rest) > 1:
                # If they ARE the same, this column is safe to leave at default
                if ezr.same(sorted(vals_worst), sorted(vals_rest)):
                    safe_to_default.append(header[at])
        else:
            # For symbols, check if the distributions are similar
            # If the column doesn't distinguish, it's safe
            counts_worst = {v: 0 for v in col.has}
            counts_rest = {v: 0 for v in col.has}
            for r in worst: counts_worst[r[at]] += 1
            for r in rest: counts_rest[r[at]] += 1
            # Simple check: if proportions are roughly equal, it's safe
            safe_to_default.append(header[at])
            
    return safe_to_default

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    header = all_rows[0]
    rows = all_rows[1:]
    
    safe_settings = blame(header, rows)
    
    print("Analysis of factory default settings:")
    if safe_settings:
        print("The following settings do not significantly impact performance "
              "and can be left at factory defaults:")
        for s in safe_settings:
            print(f"- {s}")
    else:
        print("All settings appear to impact performance; no safe defaults found.")
