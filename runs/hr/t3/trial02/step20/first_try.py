import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee record:
    1. random: Picks rows at random.
    2. rule_of_thumb: Gives biggest pay rises to the newest staff (lowest YearsAtCompany+).
    3. tenure_focus: Picks rows with the highest YearsAtCompany+ (the opposite of the rule).
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    def get_score(row_idx):
        goals = label(row_idx)
        score = 0.0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # Strategies
    # 1. Random
    # 2. Rule of thumb: Target newest staff (YearsAtCompany+ < 2)
    # 3. Tenure focus: Target longest-tenured staff (YearsAtCompany+ > 10)
    tenure_idx = header.index('YearsAtCompany+')
    
    strategies = {
        "random": lambda: random.sample(range(len(rows)), 16),
        "rule_of_thumb": lambda: [i for i, r in enumerate(rows) if r[tenure_idx] < 2.0][:17],
        "tenure_focus": lambda: sorted(range(len(rows)), key=lambda i: rows[i][tenure_idx], reverse=True)[:17]
    }

    results = {}
    best_overall_score = float('-inf')
    winner = None
    best_row_idx = -1

    for name, selector in strategies.items():
        indices = selector()
        best_strat_score = float('-inf')
        best_strat_row = -1
        
        for idx in indices:
            score = get_score(idx)
            if score > best_strat_score:
                best_strat_score = score
                best_strat_row = idx
            
            if score > best_overall_score:
                best_overall_score = score
                winner = name
                best_row_idx = idx
        
        results[name] = best_strat_score

    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                processed.append(float(val) if header[i][0].isupper() else val)
            rows.append(processed)

    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    true_goals = [[row[i] for i in goal_indices] for row in rows]
    
    # Mask goals
    for row in rows:
        for i in goal_indices:
            row[i] = "?"

    labeled = set()
    def label(i):
        if len(labeled) >= 50 and i not in labeled:
            raise Exception("Label budget exceeded")
        labeled.add(i)
        return true_goals[i]

    result = race(header, rows, label)
    
    print("Analysis: Is the 'rule of thumb' (pay rises to newest staff) effective?")
    print(f"Winner Strategy: {result['winner']}")
    print(f"The 'rule_of_thumb' strategy was compared against random sampling and tenure-focused selection.")
    if result['winner'] == 'rule_of_thumb':
        print("Conclusion: Your rule of thumb is effective for identifying high-performing arrangements.")
    else:
        print("Conclusion: Your rule of thumb is outperformed by other strategies; consider focusing on long-tenured staff instead.")
