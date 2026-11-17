import ezr
from step01 import remember


def race(header, rows, label):
    """Compare three strategies for finding a good setup."""
    
    # Strategy 1: random - pick rows at random
    def random_search():
        chosen = set()
        while len(chosen) < 50 and len(rows) > 0:
            idx = int(len(rows) * (hash(str(id())) % 100)) % len(rows)
            chosen.add(idx)
        return list(chosen)
    
    # Strategy 2: remember - use ydist to pick best rows
    def remember_search():
        tbl = ezr.Tbl([header] + rows)
        scored = [(ezr.ydist(tbl, row), i) for i, row in enumerate(rows)]
        scored.sort(key=lambda x: x[0])
        return [i for _, i in scored[:50]]
    
    # Strategy 3: spot - find suspicious/failed runs (from step09 logic)
    def spot_search():
        tbl = ezr.Tbl([header] + rows)
        scored = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
        scored.sort(key=lambda x: x[0])  # best first
        
        n_good = max(1, int(len(scored) * 0.05))
        good_rows = [rows[i] for _, i in scored[:n_good]]
        
        suspicious = []
        for rank, (ydist_val, idx) in enumerate(scored):
            row = rows[idx]
            if rank < n_good:
                continue
            
            has_unknowns = any(c == "?" for c in row)
            
            is_outlier = False
            if not has_unknowns:
                for col_name in header:
                    if col_name[0].isupper():  # numeric column
                        try:
                            val = float(row[col_name])
                            good_vals = [float(good_rows[j][col_name]) 
                                       for j in range(len(good_rows)) 
                                       if row[col_name] != "?" and good_rows[j][col_name] != "?"]
                            
                            if len(good_vals) >= 2:
                                mean_g = sum(good_vals) / len(good_vals)
                                var_g = sum((v - mean_g)**2 for v in good_vals) / (len(good_vals) - 1)
                                sd_g = var_g ** 0.5 if var_g > 0 else 1e-32
                                
                                z_score = abs(val - mean_g) / sd_g
                                if z_score > 3:
                                    is_outlier = True
                                    break
                        except (ValueError, TypeError):
                            continue
            
            if is_outlier or has_unknowns:
                suspicious.append(idx)
            
            if len(suspicious) >= 50:
                break
        
        return suspicious[:50]
    
    # Run all three strategies
    random_result = random_search()
    remember_result = remember_search()
    spot_result = spot_search()
    
    # Label the rows according to each strategy's selection
    def apply_labels(strategy, indices):
        labelled = []
        for idx in sorted(indices):
            if 0 <= idx < len(rows):
                labelled.append(label(idx))
        return labelled
    
    random_labelled = apply_labels("random", random_result)
    remember_labelled = apply_labels("remember", remember_result)
    spot_labelled = apply_labels("spot", spot_result)
    
    # Evaluate each strategy's best row
    def evaluate(tbl, rows_list):
        if not rows_list:
            return None, 0
        scored = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows_list)]
        scored.sort(key=lambda x: x[0])
        return scored[0][1], scored[0][0]
    
    tbl_random = ezr.Tbl([header] + rows)
    tbl_remember = ezr.Tbl([header] + rows)
    tbl_spot = ezr.Tbl([header] + rows)
    
    best_row, best_ydist_r = evaluate(tbl_random, random_labelled)
    best_row_r, best_ydist_rr = evaluate(tbl_remember, remember_labelled)
    best_row_s, best_ydist_ss = evaluate(tbl_spot, spot_labelled)
    
    # Determine the overall winner (lowest ydist among all strategies' best rows)
    candidates = [
        ("random", best_row_r, best_ydist_r),
        ("remember", best_row_rr, best_ydist_rr),
        ("spot", best_row_s, best_ydist_ss),
    ]
    
    # Filter out None results and find the best
    valid = [(name, row, yd) for name, row, yd in candidates if row is not None]
    
    if valid:
        valid.sort(key=lambda x: x[2])
        winner_name = valid[0][0]
        winner_row = valid[0][1]
        winner_ydist = valid[0][2]
    else:
        winner_name = "random"
        winner_row = 0
        winner_ydist = float('inf')
    
    return {
        "winner": winner_name,
        "row": winner_row,
        "tried": ["random", "remember", "spot"]
    }


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__), "Health-ClosedIssues0000.train.csv")
    rows = list(ezr.csv(path))
    header = rows[0]
    data_rows = rows[1:]

    result = race(header, data_rows, lambda i: [float(v) for v in data_rows[i][2:4]])
    print(f"Winner: {result['winner']}")
    print(f"Best row position: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
