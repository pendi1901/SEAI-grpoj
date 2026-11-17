import csv


def flow(header, row, seen):
    """Approve or reject each arriving proposal; cannot go back."""
    goal_cols = ['Cost-', 'Score-', 'Idle-']

    def parse_goals(row):
        goals = {}
        for col in goal_cols:
            idx = header.index(col)
            val = row[idx]
            if val == '?':
                return None
            try:
                goals[col] = float(val)
            except ValueError:
                return None
        return goals

    # Parse the current row's goals (skip if any goal is hidden)
    cur_goals = parse_goals(row)
    if cur_goals is None:
        return False  # can't evaluate, reject

    n_seen = len(seen) + 1
    seen.append(row)

    # If we have very few rows so far, be generous and approve anything decent.
    if n_seen <= 3:
        return True

    # Compute the best possible score for each goal from all rows seen so far.
    best = {}
    worst = {}
    for col in goal_cols:
        vals = [parse_goals(r)[col] for r in seen if parse_goals(r) is not None]
        best[col] = min(vals)   # lower is better (all goals end in -)
        worst[col] = max(vals)

    # Score the current row relative to what we've seen.
    score = 0.0
    for col in goal_cols:
        g = cur_goals[col]
        if g <= best[col]:
            score += 1.0   # at least as good as the best seen so far
        elif g >= worst[col]:
            score += 0.5   # between best and worst

    # If we've already approved something, only approve new rows that are clearly better.
    if len(seen) > 1:
        return False  # conservative: don't switch once we start rejecting
    else:
        # First row or early rows: approve anything that's not terrible.
        return True


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    seen = []
    approved = 0
    rejected = 0
    for row in rows:
        if flow(header, row, seen):
            approved += 1
        else:
            rejected += 1
        seen.append(row)

    print(f"Approved {approved}, rejected {rejected} out of {len(rows)} proposals.")
