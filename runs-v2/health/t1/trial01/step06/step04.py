def flow(header, row, seen):
    minimise_cols = [c for c in header if c.endswith('-')]
    maximise_cols = [c for c in header if c.endswith('+')]

    def score(r):
        s = 0.0
        for col in minimise_cols:
            val = r[header.index(col)]
            try:
                fval = float(val) if str(val) != '?' else None
            except (ValueError, TypeError):
                continue
            if fval is not None:
                s -= fval
        for col in maximise_cols:
            val = r[header.index(col)]
            try:
                fval = float(val) if str(val) != '?' else None
            except (ValueError, TypeError):
                continue
            if fval is not None:
                s += fval
        return s

    current_score = score(row)
    n_seen = len(seen)

    # Need a few rows to estimate the typical range before deciding
    if n_seen >= 5:
        scores_seen = [score(r) for r in seen]
        mean_s = sum(scores_seen) / len(scores_seen)
        var_s = sum((s - mean_s) ** 2 for s in scores_seen)
        std_s = var_s ** 0.5
        # Stop when current row beats the typical range by a comfortable margin
        threshold = mean_s + 1.5 * std_s
        return current_score > threshold

    return False


if __name__ == "__main__":
    import csv

    with open('Health-ClosedIssues0000.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            converted = []
            for cell in row:
                if cell.strip() == '?':
                    converted.append('?')
                else:
                    try:
                        converted.append(float(cell))
                    except ValueError:
                        converted.append(cell)
            rows.append(converted)

    chosen_idx = None
    for i, row in enumerate(rows):
        seen = rows[:i]
        if flow(header, row, seen):
            chosen_idx = i
            break

    if chosen_idx is not None:
        print(f"Row {chosen_idx} is good enough to ship.")
    else:
        print("No row was good enough; all rows examined.")
