def choose(header, rows, label):
    minimise_cols = [c for c in header if c.endswith('-')]
    maximise_cols = [c for c in header if c.endswith('+')]

    col_idx = {name: i for i, name in enumerate(header)}

    def score_from_goals(goals):
        s = 0.0
        for col in minimise_cols:
            try:
                fval = float(goals[col])
            except (ValueError, TypeError):
                continue
            if fval is not None:
                s -= fval
        for col in maximise_cols:
            try:
                fval = float(goals[col])
            except (ValueError, TypeError):
                continue
            if fval is not None:
                s += fval
        return s

    best_pos = 0
    best_score = -float('inf')
    n_tried = 0

    for i in range(len(rows)):
        if n_tried >= 50:
            break
        goals = label(i)
        sc = score_from_goals(goals)
        if sc > best_score:
            best_score = sc
            best_pos = i
        n_tried += 1

    return best_pos


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

    best_pos = choose(header, rows, label)
    print(f"Best of 50 setups tried: row {best_pos}")
