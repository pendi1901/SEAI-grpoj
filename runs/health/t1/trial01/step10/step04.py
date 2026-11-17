def flow(header, row, seen):
    """Return True if `row` is good enough to ship; False otherwise."""
    
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    def to_float(cell):
        try:
            return float(cell)
        except (ValueError, TypeError):
            return 0.0
    
    n_seen = len(seen)
    if n_seen < 10:
        # Need more data before making a decision
        return False
    
    # Track best and worst for each goal column from previously seen rows
    best_vals = []
    worst_vals = []
    for c in goal_cols:
        vals = [to_float(r[header.index(c)]) for r in seen]
        if vals:
            best_vals.append(min(vals))
            worst_vals.append(max(vals))
    
    # Evaluate current row against these ranges
    cur_vals = [to_float(row[header.index(c)]) for c in goal_cols]
    
    scores = []
    for i, (c, gv) in enumerate(zip(goal_cols, best_vals)):
        cv = cur_vals[i]
        if c.endswith('-'):
            # Minimize: lower is better; score 1.0 when equal to best
            denom = gv - worst_vals[i]
            if denom <= 0:
                scores.append(1.0)
            else:
                scores.append(max(0.0, 1.0 - (cv - gv) / denom))
        else:
            # Maximize: higher is better; score 1.0 when equal to best
            denom = best_vals[i] - worst_vals[i]
            if denom <= 0:
                scores.append(1.0)
            else:
                scores.append(max(0.0, 1.0 - (best_vals[i] - cv) / denom))
    
    avg_score = sum(scores) / len(scores)
    return avg_score >= 0.95


if __name__ == "__main__":
    import csv
    
    with open("Health-ClosedIssues0000.train.csv") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(10000)]
    
    print(f"Loaded {len(rows)} setups. Scanning for one good enough to ship...")
    
    seen = []
    for row in rows:
        if flow(header, row, seen):
            print("Found a setup good enough to ship!")
            break
        seen.append(row)
    else:
        # Exhausted all rows; pick the best one overall
        goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
        
        def to_float(cell):
            try:
                return float(cell)
            except (ValueError, TypeError):
                return 0.0
        
        best_idx = 0
        best_score = -1e9
        for i, row in enumerate(rows):
            s = 0.0
            n_goals = len(goal_cols)
            for c in goal_cols:
                v = to_float(row[header.index(c)])
                if c.endswith('-'):
                    s += v / n_goals
                else:
                    s -= v / n_goals
            if s > best_score:
                best_score = s
                best_idx = i
        
        print(f"Exhausted all rows. Best setup is row {best_idx} (score={best_score:.4f}).")
