import pandas as pd


def fix(header, row, levers):
    """Recommend changes to at least one lever for an underperforming employee."""

    goals_plus = [h for h in header if h.endswith('+')]
    goals_minus = [h for h in header if h.endswith('-')]

    # Build a reference population from the training data (loaded once)
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv")
    ref_rows = [list(r) for r in df.values]
    ref_header = list(df.columns)

    # Compute global min/max across all reference rows for goals
    col_min = {}
    col_max = {}
    for r in ref_rows:
        for c in goals_plus:
            v = float(r[c])
            col_max[c] = max(col_max.get(c, -float('inf')), v)
        for c in goals_minus:
            v = float(r[c])
            col_min[c] = min(col_min.get(c, float('inf')), v)

    # Score each reference row
    ref_scores = []
    for r in ref_rows:
        s = 0.0
        for c in goals_plus:
            lo, hi = col_min.get(c, -float('inf')), col_max.get(c, -float('inf'))
            rng = (hi - lo) or 1.0
            s += (float(r[c]) - lo) / rng
        for c in goals_minus:
            lo, hi = col_min.get(c, float('inf')), col_max.get(c, float('inf'))
            rng = (hi - lo) or 1.0
            s += (hi - float(r[c])) / rng
        ref_scores.append(s)

    # Score the bad row using its actual goal values (no "?" for goals in this scenario)
    s_bad = 0.0
    for c in goals_plus:
        lo, hi = col_min.get(c, -float('inf')), col_max.get(c, -float('inf'))
        rng = (hi - lo) or 1.0
        s_bad += (float(row[c]) - lo) / rng
    for c in goals_minus:
        lo, hi = col_min.get(c, float('inf')), col_max.get(c, float('inf'))
        rng = (hi - lo) or 1.0
        s_bad += (hi - float(row[c])) / rng

    # Determine which lever to change based on the row's weakest goal gap
    # Map lever names to their '+' or '-' goal column
    lever_map = {
        'travel': 'businessTravel',
        'overtime': 'overTime',
        'training': 'TrainingTimesLastYear',
        'pay_rise': 'PercentSalaryHike',
        'stock': 'StockOptionLevel',
    }

    # For each lever, compute how much the row's score would improve if we set it to its best value
    candidate_changes = []
    for lever_name, goal_col in lever_map.items():
        if goal_col not in levers:
            continue
        lo, hi = col_min.get(goal_col, -float('inf')), col_max.get(goal_col, float('inf'))
        rng = (hi - lo) or 1.0

        # Current contribution of this goal to the bad row's score
        current_val = float(row[goal_col])
        if goal_col in goals_plus:
            cur_contrib = (current_val - lo) / rng
        else:
            cur_contrib = (hi - current_val) / rng

        # Best possible contribution
        best_val = levers[lever_name]
        if isinstance(best_val, tuple):
            best_val = float(best_val[1])  # high for '+' goals
        elif goal_col in goals_minus:
            best_val = float(best_val)
        else:
            best_val = float(best_val)

        new_contrib = (best_val - lo) / rng if goal_col in goals_plus else (hi - best_val) / rng
        improvement = new_contrib - cur_contrib

        candidate_changes.append((improvement, lever_name))

    # Pick the lever with the largest positive impact; fall back to first if none improve
    candidate_changes.sort(key=lambda x: x[0], reverse=True)
    chosen_improvement, chosen_lever = candidate_changes[0]

    result = {}
    if chosen_improvement > 0:
        best_val = levers[chosen_lever]
        if isinstance(best_val, tuple):
            result[chosen_lever] = str(best_val[1])
        else:
            result[chosen_lever] = str(best_val)
    else:
        # No lever improves; pick the one with least negative impact (closest to 0)
        chosen_improvement, chosen_lever = candidate_changes[-1]
        best_val = levers[chosen_lever]
        if isinstance(best_val, tuple):
            result[chosen_lever] = str(best_val[1])
        else:
            result[chosen_lever] = str(best_val)

    return result


if __name__ == "__main__":
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]

    # Pick a bad row (one who left, i.e., attrition='Yes')
    bad_rows = [r for r in rows if r[1] == 'Yes']  # column index 1 is attrition
    sample_bad = bad_rows[0]

    levers = {
        'travel': ['Travel_Rarely', 'Non-Travel'],
        'overtime': ['N', 'Y'],
        'training': [0, 5],
        'pay_rise': [0, 100],
        'stock': [0, 4],
    }

    recommendation = fix(header, sample_bad, levers)
    print("Recommended changes for an employee who left:")
    for lever, new_val in recommendation.items():
        print(f"  {lever}: change to '{new_val}'")
