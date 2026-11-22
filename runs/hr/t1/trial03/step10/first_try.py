import csv
import random

def get_goal_indices(header):
    return [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]

def get_score(header, row_goals, goal_indices, min_vals, max_vals):
    scores = []
    for i, idx in enumerate(goal_indices):
        rng = max_vals[idx] - min_vals[idx]
        rng = rng if rng != 0 else 1
        norm = (row_goals[i] - min_vals[idx]) / rng
        if header[idx].endswith('-'):
            norm = 1 - norm
        scores.append(norm)
    return sum(scores) / len(scores)

def race(header, rows, label):
    goal_indices = get_goal_indices(header)
    # Budget: 50 labels total
    budget = 50
    strategies = ["random", "tenure_focused", "satisfaction_focused"]
    
    # Pre-calculate global min/max for scoring
    # We use a small sample to estimate global bounds for normalization
    sample_indices = random.sample(range(len(rows)), min(100, len(rows)))
    all_goals = [label(i) for i in sample_indices]
    min_vals = {idx: min(g[i] for g in all_goals) for i, idx in enumerate(goal_indices)}
    max_vals = {idx: max(g[i] for g in all_goals) for i, idx in enumerate(goal_indices)}

    results = {}
    
    # 1. Random Strategy
    rand_indices = random.sample(range(len(rows)), budget // 3)
    best_rand_idx = -1
    best_rand_score = -1.0
    for i in rand_indices:
        score = get_score(header, label(i), goal_indices, min_vals, max_vals)
        if score > best_rand_score:
            best_rand_score = score
            best_rand_idx = i
    results["random"] = (best_rand_idx, best_rand_score)

    # 2. Tenure Focused (Look for high YearsAtCompany+)
    yac_idx = header.index('YearsAtCompany+')
    tenure_indices = sorted(range(len(rows)), key=lambda i: rows[i][yac_idx], reverse=True)[:budget // 3]
    best_ten_idx = -1
    best_ten_score = -1.0
    for i in tenure_indices:
        score = get_score(header, label(i), goal_indices, min_vals, max_vals)
        if score > best_ten_score:
            best_ten_score = score
            best_ten_idx = i
    results["tenure_focused"] = (best_ten_idx, best_ten_score)

    # 3. Satisfaction Focused (Look for high JobSatisfaction)
    js_idx = header.index('JobSatisfaction')
    sat_indices = sorted(range(len(rows)), key=lambda i: rows[i][js_idx], reverse=True)[:budget // 3]
    best_sat_idx = -1
    best_sat_score = -1.0
    for i in sat_indices:
        score = get_score(header, label(i), goal_indices, min_vals, max_vals)
        if score > best_sat_score:
            best_sat_score = score
            best_sat_idx = i
    results["satisfaction_focused"] = (best_sat_idx, best_sat_score)

    # Determine winner
    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": strategies}

def load_data(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    goal_indices = get_goal_indices(header)
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    outcome = race(header, rows, label)
    print(f"Winner: {outcome['winner']}")
    print(f"Best row found: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
