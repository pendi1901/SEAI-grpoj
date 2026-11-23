import csv
import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (local search), and surrogate-guided.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i, h in enumerate(header) if not h.endswith(('-', '+'))]
    
    def get_score(row_goals):
        score = 0
        for i, val in enumerate(row_goals):
            if header[goal_indices[i]].endswith('-'):
                score -= val
            else:
                score += val
        return score

    labeled = {} # index: score

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise Exception("Budget exceeded")
            labeled[i] = get_score(label(i))
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        for _ in range(16):
            get_label(random.randint(0, len(rows) - 1))

    # Strategy 2: Greedy (Hill Climbing)
    def strategy_greedy():
        curr = random.randint(0, len(rows) - 1)
        for _ in range(16):
            best_n, best_s = -1, -float('inf')
            for _ in range(5):
                n = random.randint(0, len(rows) - 1)
                s = get_label(n)
                if s > best_s:
                    best_s, best_n = s, n
            if best_s > get_label(curr):
                curr = best_n

    # Strategy 3: Surrogate (Random Forest)
    def strategy_surrogate():
        # Use existing labels if any
        if len(labeled) < 5:
            for _ in range(5): get_label(random.randint(0, len(rows) - 1))
        
        for _ in range(15):
            X = [[rows[i][j] for j in input_indices] for i in labeled.keys()]
            y = list(labeled.values())
            model = RandomForestRegressor(n_estimators=10).fit(X, y)
            
            best_idx, best_pred = -1, -float('inf')
            for i in range(len(rows)):
                if i not in labeled:
                    pred = model.predict([[rows[i][j] for j in input_indices]])[0]
                    if pred > best_pred:
                        best_pred, best_idx = pred, i
            get_label(best_idx)

    strategies = {"random": strategy_random, "greedy": strategy_greedy, "surrogate": strategy_surrogate}
    for name, func in strategies.items():
        func()

    best_idx = max(labeled, key=labeled.get)
    return {"winner": max(strategies.keys(), key=lambda n: max([labeled[i] for i in labeled])), 
            "row": best_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [[float(x) for x in r] for r in reader]
    
    true_goals = [[r[i] for i, h in enumerate(header) if h.endswith(('-', '+'))] for r in data]
    masked_rows = [[("?" if h.endswith(('-', '+')) else r[i]) for i, h in enumerate(header)] for r in data]
    
    def label(i): return true_goals[i]
    
    result = race(header, masked_rows, label)
    print(f"Race Results: The winning strategy is '{result['winner']}'.")
    print(f"Best setup found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
