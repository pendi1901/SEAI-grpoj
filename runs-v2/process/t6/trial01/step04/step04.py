import ezr

def flow(header, row, seen):
    """Approve or reject a proposal that just arrived."""
    tbl = ezr.Tbl([header] + [list(r) for r in seen])
    
    # Compute ydist for the current row and all seen rows
    cur_y = ezr.ydist(tbl, list(row))
    
    if not seen:
        # First row - approve to establish a baseline
        return True
    
    # Build tree on approved rows from seen (we track them in flow)
    # For simplicity, use the mean ydist of seen as reference
    best_y = min(ezr.ydist(tbl, list(r)) for r in seen)
    
    if cur_y <= best_y:
        return True
    return False

if __name__ == "__main__":
    import os
    path = 'pom3a.train.csv'
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(',')
    rows = ezr.csv(path)
    
    approved = []
    rejected = 0
    
    for row in rows:
        row_list = list(row)
        decision = flow(header, row_list, [list(r) for r in approved])
        if decision:
            approved.append(row_list)
        else:
            rejected += 1
    
    print(f"Approved {len(approved)} of {len(rows)} proposals; "
          f"{rejected} rejected.")
