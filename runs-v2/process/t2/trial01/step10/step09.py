from step01 import remember


def spot(header, rows):
    """Return positions of rows with mistyped/made-up input values."""
    goals = [c for c in header if c.endswith('-') and c[0].isupper()]
    
    n = len(rows)
    if n == 0:
        return []

    # Identify numeric vs symbolic columns (excluding goals)
    input_cols = [c for c in header if c not in goals]
    
    suspicious_rows = set()
    
    for col in input_cols:
        vals = []
        for i, row in enumerate(rows):
            v = row[header.index(col)]
            if isinstance(v, (int, float)):
                vals.append((v, i))
        
        if len(vals) < 2:
            continue
        
        values = [x[0] for x in vals]
        indices = [x[1] for x in vals]
        
        mean_val = sum(values) / len(values)
        std_val = (sum((v - mean_val)**2 for v in values) / len(values)) ** 0.5
        
        if std_val < 1e-12:
            continue
        
        # Flag rows where value is more than 2 std from mean
        for i, row in enumerate(rows):
            v = row[header.index(col)]
            if isinstance(v, (int, float)):
                z = abs(v - mean_val) / std_val
                if z > 2.0:
                    suspicious_rows.add(i)

    return sorted(suspicious_rows, reverse=True)


if __name__ == "__main__":
    import csv
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    suspicious = spot(header, rows)
    print(f"Suspicious rows (most to least): {suspicious}")
