import csv
import random
from step01 import remember

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (local search), and smart (remember-based).
    Budget: 50 labels total.
    """
    budget = 50
    labeled = {}

    def get_goals(idx):
        if idx not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[idx] = label(idx)
        return labeled[idx]

    def score_row(idx):
        goals = get_goals(idx)
        # Normalize goals using global bounds (approximate from first 50 if needed, 
        # but here we use the row's own goals relative to others)
        # For simplicity, we use the remember logic:
        row_with_goals = list(rows[idx])
        goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for i, g_idx in enumerate(goal_indices):
            row_with_goals[g_idx] = goals[i]
        return row_with_goals

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx = indices[0]
        best_score = -float('inf')
        for idx in indices:
            r = score_row(idx)
            # Simple score: (1-MRE) + ACC + PRED
            s = (1 - r[0]) + r[1] + r[2]
            if s > best_score:
                best_score, best_idx = s, idx
        return best_idx

    # 2. Greedy Strategy (Hill Climbing)
    def strategy_greedy():
        curr = random.randint(0, len(rows) - 1)
        for _ in range(16):
            neighbors = random.sample(range(len(rows)), 5)
            best_n = curr
            best_s = (1 - score_row(curr)[0]) + score_row(curr)[1] + score_row(curr)[2]
            for n in neighbors:
                s = (1 - score_row(n)[0]) + score_row(n)[1] + score_row(n)[2]
                if s > best_s:
                    best_s, best_n = s, n
            curr = best_n
        return curr

    # 3. Smart Strategy (Sample + Remember)
    def strategy_smart():
        indices = random.sample(range(len(rows)), 18)
        data = [score_row(i) for i in indices]
        best_local = remember(header, data)[0]
        return indices[best_local]

    strategies = {"random": strategy_random, "greedy": strategy_greedy, "smart": strategy_smart}
    results = {}
    for name, func in strategies.items():
        idx = func()
        r = score_row(idx)
        results[name] = {"idx": idx, "score": (1 - r[0]) + r[1] + r[2]}

    winner = max(results, key=lambda n: results[n]["score"])
    return {"winner": winner, "row": results[winner]["idx"], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])

    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    true_goals = [[r[i] for i in goal_indices] for r in rows]
    
    masked_rows = []
    for r in rows:
        masked = list(r)
        for i in goal_indices: masked[i] = "?"
        masked_rows.append(masked)

    result = race(header, masked_rows, lambda i: true_goals[i])
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
