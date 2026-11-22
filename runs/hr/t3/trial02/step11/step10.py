import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee record:
    1. random: Picks rows at random.
    2. extreme: Picks rows with the highest 'TotalWorkingYears'.
    3. balanced: Picks rows with 'JobSatisfaction' >= 3.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    def get_score(row_idx):
        goals = label(row_idx)
        score = 0.0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            # Normalize: + is better high, - is better low
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    strategies = {
        "random": lambda: random.sample(range(len(rows)), 16),
        "extreme": lambda: sorted(range(len(rows)), key=lambda i: rows[i][header.index('TotalWorkingYears')], reverse=True)[:17],
        "balanced": lambda: [i for i, r in enumerate(rows) if r[header.index('JobSatisfaction')] >= 3][:17]
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
    
    print(f"Race Results:")
    print(f"Winner Strategy: {result['winner']}")
    print(f"Best Row Found Index: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
    print(f"Total Labels Used: {len(labeled)}")
