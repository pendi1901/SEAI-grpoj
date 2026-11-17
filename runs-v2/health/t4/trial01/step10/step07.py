def choose(header, rows, label):
    goal_names = [c for c in header if c.endswith('-') or c.endswith('+')]

    best_pos = 0
    best_score = float('inf')

    for i in range(50):
        goals = label(i)
        score = 0.0
        for j, g_name in enumerate(goal_names):
            v = float(goals[j]) if isinstance(goals[j], str) else goals[j]
            if '-' in g_name:
                score += v          # minimise MRE-
            else:
                score -= v          # maximise ACC+, PRED40+

        if score < best_score:
            best_score = score
            best_pos = i

    return best_pos


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)

    result = choose(header, [], lambda i: [df.iloc[i]['MRE-'], df.iloc[i]['ACC+'], df.iloc[i]['PRED40+']])
    print(f"Best setup is row {result}: MRE={df.iloc[result]['MRE-']:.4f}, ACC={df.iloc[result]['ACC+']:.4f}, PRED40={df.iloc[result]['PRED40+']:.4f}")
