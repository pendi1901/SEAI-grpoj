import csv
import random

def get_goal_indices(header):
    return [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]

def get_score(header, row_goals, goal_indices):
    """
    Calculates a normalized score [0, 1] for a row based on goal columns.
    Since we don't have global min/max, we use a fixed heuristic range 
    based on the dataset's typical values for these specific columns.
    """
    # Typical ranges for the goal columns in this dataset
    # YearsAtCompany: 0-40, YearsInCurrentRole: 0-20, YearsWithCurrManager: 0-20
    ranges = {
        'YearsAtCompany+': (0, 40),
        'YearsInCurrentRole+': (0, 20),
        'YearsWithCurrManager+': (0, 20)
    }
    
    scores = []
    for i, idx in enumerate(goal_indices):
        name = header[idx]
        low, high = ranges.get(name, (0, 40))
        rng = high - low if high != low else 1
        norm = (row_goals[i] - low) / rng
        if name.endswith('-'):
            norm = 1 - norm
        scores.append(max(0, min(1, norm)))
    return sum(scores) / len(scores)

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee arrangement.
    Total budget: 50 labels.
    """
    goal_indices = get_goal_indices(header)
    strategies = ["random", "tenure_priority", "satisfaction_priority"]
    
    # We split 50 labels across 3 strategies: 16, 17, 17
    budgets = [16, 17, 17]
    results = {}
    
    # 1. Random
    indices_rand = random.sample(range(len(rows)), budgets[0])
    best_rand_idx, best_rand_score = -1, -1.0
    for i in indices_rand:
        score = get_score(header, label(i), goal_indices)
        if score > best_rand_score:
            best_rand_score, best_rand_idx = score, i
    results["random"] = (best_rand_idx, best_rand_score)
    
    # 2. Tenure Priority (Sort by YearsAtCompany+)
    yac_idx = header.index('YearsAtCompany+')
    indices_ten = sorted(range(len(rows)), key=lambda i: rows[i][yac_idx], reverse=True)[:budgets[1]]
    best_ten_idx, best_ten_score = -1, -1.0
    for i in indices_ten:
        score = get_score(header, label(i), goal_indices)
        if score > best_ten_score:
            best_ten_score, best_ten_idx = score, i
    results["tenure_priority"] = (best_ten_idx, best_ten_score)
    
    # 3. Satisfaction Priority (Sort by JobSatisfaction)
    js_idx = header.index('JobSatisfaction')
    indices_sat = sorted(range(len(rows)), key=lambda i: rows[i][js_idx], reverse=True)[:budgets[2]]
    best_sat_idx, best_sat_score = -1, -1.0
    for i in indices_sat:
        score = get_score(header, label(i), goal_indices)
        if score > best_sat_score:
            best_sat_score, best_sat_idx = score, i
    results["satisfaction_priority"] = (best_sat_idx, best_sat_score)
    
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
