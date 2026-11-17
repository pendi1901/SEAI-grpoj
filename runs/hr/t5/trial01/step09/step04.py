import ezr

def flow(header, row, seen):
    """Returns True if this person needs a 'what would keep you here' conversation."""
    goals = [header[i] for i in range(len(header)) if header[i][-1] in '+-']

    def goal_distance(row):
        s = 0.0
        for col_name in goals:
            idx = header.index(col_name)
            v = row[idx]
            target = 1.0 if col_name[-1] == '+' else 0.0
            try:
                s += abs(float(v) - target)
            except (ValueError, TypeError):
                pass
        return s

    score = goal_distance(row)
    attr_idx = header.index('attrition')
    if row[attr_idx] == 'No':
        return False
    n_goals = len(goals)
    threshold = 0.5 * n_goals
    return score > threshold


if __name__ == "__main__":
    import csv

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    flagged = 0
    for row in rows:
        if flow(header, row, []):
            flagged += 1

    print(f"Flagged {flagged} of {len(rows)} employees for 'what would keep you here' conversations.")
