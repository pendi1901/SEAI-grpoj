import csv


def race(header, rows, label):
    """Compare three strategies for finding the best employee among up to 50 interviews."""

    goal_cols = [c for c in header if c.endswith('+')]
    attrition_idx = None
    for i, col in enumerate(header):
        if col == 'attrition':
            attrition_idx = i
            break

    def score_row(row):
        """Compute a row's quality: sum of goal values (higher is better)."""
        s = 0.0
        for col in goal_cols:
            cell = row[header.index(col)]
            if cell == '?':
                continue
            try:
                v = float(cell)
            except ValueError:
                v = 0.0
            s += v
        return s

    def strategy_random():
        """Pick rows at random from those with attrition='No'."""
        candidates = []
        for i, row in enumerate(rows):
            if attrition_idx is not None and row[attrition_idx] == 'No':
                candidates.append(i)
        # Shuffle to get a random subset
        import random as _r
        _r.shuffle(candidates)
        chosen = candidates[:50]
        best_pos = -1
        best_score = float('-inf')
        for pos in chosen:
            s = score_row(rows[pos])
            if s > best_score:
                best_score = s
                best_pos = pos
        return best_pos

    def strategy_greedy():
        """Pick rows with highest tenure (YearsAtCompany+) first."""
        candidates = []
        for i, row in enumerate(rows):
            if attrition_idx is not None and row[attrition_idx] == 'No':
                year_val = 0.0
                try:
                    year_col = header.index('YearsAtCompany+')
                    cell = row[year_col]
                    if cell != '?':
                        year_val = float(cell)
                except (ValueError, IndexError):
                    pass
                candidates.append((year_val, i))
        candidates.sort(key=lambda x: -x[0])
        chosen = [c[1] for c in candidates[:50]]
        best_pos = -1
        best_score = float('-inf')
        for pos in chosen:
            s = score_row(rows[pos])
            if s > best_score:
                best_score = s
                best_pos = pos
        return best_pos

    def strategy_blind():
        """Pick rows with highest satisfaction scores first."""
        candidates = []
        for i, row in enumerate(rows):
            if attrition_idx is not None and row[attrition_idx] == 'No':
                sat_sum = 0.0
                for col in goal_cols:
                    cell = row[header.index(col)]
                    if cell != '?':
                        try:
                            sat_sum += float(cell)
                        except ValueError:
                            pass
                candidates.append((sat_sum, i))
        candidates.sort(key=lambda x: -x[0])
        chosen = [c[1] for c in candidates[:50]]
        best_pos = -1
        best_score = float('-inf')
        for pos in chosen:
            s = score_row(rows[pos])
            if s > best_score:
                best_score = s
                best_pos = pos
        return best_pos

    # Run all three strategies and collect results.
    tried = ['random', 'greedy', 'blind']
    results = {name: None for name in tried}

    for name in tried:
        if name == 'random':
            results[name] = strategy_random()
        elif name == 'greedy':
            results[name] = strategy_greedy()
        else:
            results[name] = strategy_blind()

    # Find the best result across all strategies.
    best_name = None
    best_row = -1
    best_score = float('-inf')
    for name in tried:
        pos = results[name]
        if pos is not None and pos >= 0:
            s = score_row(rows[pos])
            if s > best_score:
                best_score = s
                best_name = name
                best_row = pos

    return {
        'winner': best_name,
        'row': best_row,
        'tried': tried,
    }


if __name__ == '__main__':
    with open('WA_Fn-UseC_-HR-Employee-Attrition.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    result = race(header, rows, label)
    print(
        "Among three strategies (random, greedy, blind), the winner is "
        + f"'{result['winner']}', which found row {result['row']}."
    )
