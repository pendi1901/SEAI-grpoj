def choose(header, rows, label):
    goal_cols = ['Cost-', 'Score-', 'Idle-']

    def is_goal(col):
        return col.endswith('-') and col != '-'

    n_rows = len(rows)
    if n_rows == 0:
        return 0

    max_trials = min(50, n_rows)

    best_idx = -1
    best_score = float('inf')

    for i in range(max_trials):
        goals = label(i)
        score = sum(float(goals[col]) for col in goal_cols)
        if score < best_score:
            best_score = score
            best_idx = i

    return best_idx


if __name__ == "__main__":
    import csv

    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [list(map(float, row)) for row in reader]

    result = choose(header, rows, lambda i: [rows[i][header.index(col)] for col in ['Cost-', 'Score-', 'Idle-']])
    print(f"Best setup index: {result}  (score={best_score:.4f})")
