import csv
import random
import step06

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee row.
    Budget: 50 labels total.
    """
    budget = 50
    used_indices = {}

    def get_true_goals(idx):
        if idx not in used_indices:
            if len(used_indices) >= budget:
                return [0.0] * len([h for h in header if h.endswith('+') or h.endswith('-')])
            used_indices[idx] = label(idx)
        return used_indices[idx]

    def get_score(idx):
        goals = get_true_goals(idx)
        score = 0
        goal_ptr = 0
        for name in header:
            if name.endswith('+'):
                score += goals[goal_ptr]
                goal_ptr += 1
            elif name.endswith('-'):
                score -= goals[goal_ptr]
                goal_ptr += 1
        return score

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx = -1
        best_score = float('-inf')
        for idx in indices:
            s = get_score(idx)
            if s > best_score:
                best_score, best_idx = s, idx
        return best_idx, best_score

    # Strategy 2: Rule of Thumb (Biggest pay rises to newest staff)
    # Newest staff = low TotalWorkingYears, biggest pay rise = high PercentSalaryHike
    def strategy_rule_of_thumb():
        tenure_idx = header.index('TotalWorkingYears')
        hike_idx = header.index('PercentSalaryHike')
        # Score = (Hike) - (Tenure)
        sorted_rows = sorted(range(len(rows)), key=lambda i: rows[i][hike_idx] - rows[i][tenure_idx], reverse=True)
        best_idx = -1
        best_score = float('-inf')
        for idx in sorted_rows[:budget // 3]:
            s = get_score(idx)
            if s > best_score:
                best_score, best_idx = s, idx
        return best_idx, best_score

    # Strategy 3: High Tenure (Greedy on TotalWorkingYears)
    def strategy_tenure():
        tenure_idx = header.index('TotalWorkingYears')
        sorted_rows = sorted(range(len(rows)), key=lambda i: rows[i][tenure_idx], reverse=True)
        best_idx = -1
        best_score = float('-inf')
        for idx in sorted_rows[:budget // 3]:
            s = get_score(idx)
            if s > best_score:
                best_score, best_idx = s, idx
        return best_idx, best_score

    strategies = {
        "random": strategy_random,
        "rule_of_thumb": strategy_rule_of_thumb,
        "tenure": strategy_tenure
    }

    results = {}
    for name, func in strategies.items():
        idx, score = func()
        results[name] = (idx, score)

    winner = max(results, key=lambda n: results[n][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    result = race(header, rows, label)
    print(f"The winning strategy is: {result['winner']}")
    print("The 'rule of thumb' (giving pay rises to new staff) was compared against random selection and tenure-based selection.")
    if result['winner'] == 'rule_of_thumb':
        print("Result: Your rule of thumb is effective.")
    else:
        print(f"Result: The {result['winner']} strategy outperformed your rule of thumb.")
