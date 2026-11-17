def spot(header, rows):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if not c.endswith('-') and not c.endswith('+')]
    
    n = len(rows)
    suspicious = []
    
    # For each numeric column, compute statistics from valid rows
    col_stats = {}
    for col in input_cols + goal_cols:
        vals = []
        for row in rows:
            v = row[header.index(col)]
            if v == '?':
                continue
            try:
                vals.append(float(v))
            except (ValueError, TypeError):
                continue
        
        if len(vals) < 2:
            col_stats[col] = {'mean': 0.0, 'std': 1.0}
            continue
        
        import statistics
        mean_val = sum(vals) / len(vals)
        variance = sum((x - mean_val)**2 for x in vals) / (len(vals) - 1) if len(vals) > 1 else 0.0
        std_val = variance**0.5
        
        col_stats[col] = {'mean': mean_val, 'std': std_val}
    
    # For each row, check if any value is an outlier
    for i, row in enumerate(rows):
        max_deviation = 0.0
        for col in header:
            v = row[header.index(col)]
            if v == '?':
                continue
            try:
                fv = float(v)
            except (ValueError, TypeError):
                continue
            
            stats = col_stats[col]
            deviation = abs(fv - stats['mean']) / max(stats['std'], 1e-9)
            
            if deviation > max_deviation:
                max_deviation = deviation
        
        # Flag rows with high deviations in input columns
        for col in input_cols:
            v = row[header.index(col)]
            if v == '?':
                continue
            try:
                fv = float(v)
            except (ValueError, TypeError):
                continue
            
            stats = col_stats[col]
            deviation = abs(fv - stats['mean']) / max(stats['std'], 1e-9)
            
            if deviation > 3.0:  # More than 3 standard deviations
                suspicious.append(i)
    
    return sorted(suspicious, reverse=True)[:n]
