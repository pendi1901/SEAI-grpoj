import csv


def fix(header, row, levers):
    """Return {column: new_value} for the smallest change that rescues a bad row."""
    goals = [c for c in header if c.endswith('-') and c[0].isupper()]

    # Identify which goal columns are currently bad (above their best).
    n = len(row)
    current_score = sum(float(row[header.index(g)]) for g in goals)

    # For each lever, compute how much the score improves if we pick the extreme value.
    improvements = {}  # {lever: max improvement}
    for col, values in levers.items():
        best_improve = -float('inf')
        for v in values:
            new_row = list(row)
            idx = header.index(col)
            if isinstance(v, (int, float)):
                new_row[idx] = v
            else:
                new_row[idx] = v
            new_score = sum(float(new_row[header.index(g)]) for g in goals)
            improve = current_score - new_score  # positive means better
            best_improve = max(best_improve, improve)
        improvements[col] = best_improve

    if not improvements:
        return {}

    # Pick the lever with the largest improvement.
    chosen = max(improvements, key=improvements.get)
    new_val = None
    for v in levers[chosen]:
        new_row = list(row)
        idx = header.index(chosen)
        if isinstance(v, (int, float)):
            new_row[idx] = v
        else:
            new_row[idx] = v
        new_score = sum(float(new_row[header.index(g)]) for g in goals)
        improve = current_score - new_score
        if improve > 0:
            new_val = v
            break

    return {chosen: new_val}


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # Use a bad row (one of the worst).
    goals = [c for c in header if c.endswith('-') and c[0].isupper()]
    scored = [(sum(float(row[header.index(g)]) for g in goals), i) for i, row in enumerate(rows)]
    scored.sort(reverse=True)
    bad_row = rows[scored[0][1]]

    # Determine levers: numeric columns get (low, high); symbolic get all values.
    import random
    levers = {}
    for col in header:
        if col.endswith('-') and col[0].isupper():
            continue  # goals are not levers
        vals = [float(x) for x in bad_row]
        if any(isinstance(v, str) for v in vals):
            levers[col] = list(vals)
        else:
            lo = min(vals) - 0.1
            hi = max(vals) + 0.1
            levers[col] = (lo, hi)

    result = fix(header, bad_row, levers)
    print(f"Rescue plan: change {list(result.keys())[0]} to {result[list(result.keys())[0]]}")
