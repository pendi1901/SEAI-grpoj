import ezr
from step01 import remember


def fix(header, row, levers):
    """Find the smallest lever-change that makes a bad row acceptable."""
    
    # Identify which columns are goals (names ending in - or +)
    goal_cols = [c for c in header if c[-1] in '-+']
    
    # Build a tree on all rows to understand what makes good setups
    tbl_all = ezr.Tbl([header] + row[:len(header)])  # placeholder, will be rebuilt
    
    # Get the best known setup from earlier steps
    path = "Health-ClosedIssues0000.train.csv"
    if not hasattr(fix, '_rows'):
        import os
        rows_all = list(ezr.csv(path))
        header_real = rows_all[0]
        data_rows = rows_all[1:]
        fix._header = header_real
        fix._rows = data_rows
    
    tbl_ref = ezr.Tbl([fix._header] + fix._rows)
    
    # Score the original row against reference
    ydist_orig = ezr.ydist(tbl_ref, row)
    
    # Try each lever combination (smallest change first)
    best_change = None
    best_ydist = float('inf')
    
    for col_name, values in levers.items():
        if len(values) == 2:
            low, high = values
            # For numeric columns, try a few intermediate points
            candidates = [low]
            n_steps = max(1, int((high - low) / 0.5))
            for i in range(n_steps + 1):
                t = i / n_steps
                val = low + t * (high - low)
                candidates.append(val)
            candidates.append(high)
        else:
            candidates = values
        
        # Try changing just this column
        test_row = list(row)
        for val in candidates:
            if col_name[-1] == '-':
                ydist_test = ezr.ydist(tbl_ref, test_row)
                if ydist_test < best_ydist and ydist_test <= 0.5:
                    best_change = {col_name: val}
                    best_ydist = ydist_test
            
            # Also try with other columns unchanged but this one changed
            if col_name in goal_cols:
                test_row[col_name] = val
    
    # If no single lever change works, try combinations of 2
    if best_change is None and len(levers) > 1:
        for i in range(len(levers)):
            for j in range(i + 1, len(levers)):
                col1, col2 = list(levers.keys())[i], list(levers.keys())[j]
                vals1, vals2 = levers[col1], levers[col2]
                
                if len(vals1) == 2 and len(vals2) == 2:
                    for v1 in [vals1[0], vals1[1]]:
                        for v2 in [vals2[0], vals2[1]]:
                            test_row = list(row)
                            test_row[col1] = v1
                            test_row[col2] = v2
                            ydist_test = ezr.ydist(tbl_ref, test_row)
                            if ydist_test < best_ydist and ydist_test <= 0.5:
                                best_change = {col1: v1, col2: v2}
                                best_ydist = ydist_test
    
    return best_change


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__), "Health-ClosedIssues0000.train.csv")
    rows = list(ezr.csv(path))
    header = rows[0]
    data_rows = rows[1:]

    # Find a bad row (high ydist)
    scored = [(ezr.ydist(ezr.Tbl([header] + r), r), i) for i, r in enumerate(data_rows)]
    scored.sort(key=lambda x: -x[0])  # worst first
    
    if scored and scored[0][0] > 0.5:
        bad_row = data_rows[scored[0][1]]
        print(f"Found a bad setup (ydist={scored[0][0]:.4f})")
        
        # Determine which levers are available (numeric columns with ranges, symbolic with values)
        numeric_cols = {c: r[c] for c in header if isinstance(r[c], float)}
        print(f"Numeric columns and their current values:")
        for col, val in numeric_cols.items():
            print(f"  {col}: {val}")
