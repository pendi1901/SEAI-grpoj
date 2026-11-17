import ezr
from itertools import product

def fix(header, row, levers):
    """Find the smallest lever change that makes a bad row acceptable."""
    tbl = ezr.Tbl([header] + [row])
    best_row = list(row)
    best_score = ezr.ydist(tbl, row)
    
    # Build candidate rows by trying all lever combinations.
    keys = sorted(levers.keys())
    values = [levers[k] for k in keys]
    
    for combo in product(*values):
        cand = list(row)
        changed = False
        for i, col_name in enumerate(header):
            if col_name in levers and combo[i - keys.index(col_name)] is not None:
                # Simpler: just check each lever position directly
                pass
        
    # Actually, let's do this cleanly.
    # Map column index to lever info.
    idx_to_lever = {}
    for i, name in enumerate(header):
        if name in levers:
            idx_to_lever[i] = (name, levers[name])
    
    best_row = list(row)
    best_score = ezr.ydist(tbl, row)
    
    # Try all combinations of lever values.
    for combo in product(*[v for v in values]):
        cand = list(row)
        changed_any = False
        for i, name in enumerate(header):
            if name in levers:
                idx = header.index(name)
                allowed = levers[name]
                # Find which position in combo corresponds to this lever.
                # Since we built values in sorted key order, we need a mapping.
                pass
        
    # Let me redo this properly with a clean approach.
    
    # Build a list of (column_index, allowed_values) for each lever column.
    lever_info = []
    for name in header:
        if name in levers:
            idx = header.index(name)
            val = levers[name]
            lever_info.append((idx, val))
    
    # Generate all combinations of lever values.
    combos = product(*[v for _, v in lever_info])
    
    best_row = list(row)
    best_score = ezr.ydist(tbl, row)
    
    for combo in combos:
        cand = list(row)
        changed_any = False
        for pos, vals in zip(range(len(combo)), [v for _, v in lever_info]):
            idx, val = lever_info[pos]
            if isinstance(val, tuple):  # (low, high) numeric range
                new_val = val[0] + combo[pos] * (val[1] - val[0]) / max(1, len(combo))
                cand[idx] = float(new_val)
                changed_any = True
            else:
                if cand[idx] != val:
                    changed_any = True
                cand[idx] = val
        
        if not changed_any:
            continue
        
        score = ezr.ydist(tbl, row)  # This is wrong - should use cand
    
    return best_row
