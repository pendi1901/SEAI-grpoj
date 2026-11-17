def justify(header, rows, row):
    goals_min = [c for c in header if c.endswith('-')]
    goals_max = [c for c in header if c.endswith('+')]

    def score_row(r):
        s = sum(float(r[header.index(g)]) for g in goals_min) + \
             sum(-float(r[header.index(g)]) for g in goals_max)
        return s

    scores = [(score_row(r), r) for r in rows]
    scores.sort(reverse=True)
    threshold = scores[int(len(scores) * 0.25)][0]

    p = sum(1 for _, r in scores if score_row(row) >= threshold) / len(rows)
    reason = (
        f"Among {len(rows)} employees, this person's goal alignment is at the top "
        f"{int(p * 100)}% — they rank better than most of their peers."
    )
    return p, reason


if __name__ == "__main__":
    import csv

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    test_row = ["?"] * len(header)
    p, reason = justify(header, rows, test_row)
    print(f"Top-quartile ranking: {p:.2%} — {reason}")
