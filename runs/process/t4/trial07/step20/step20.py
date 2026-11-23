import csv
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def get_score(header, row_goals):
    """Calculates a normalized aggregate score for a row."""
    goals = [col for col in header if col.endswith(('-', '+'))]
    scores = []
    for i, goal in enumerate(goals):
        val = row_goals[i]
        if goal.endswith('-'):
            scores.append(1.0 - val)
        else:
            scores.append(val)
    return np.mean(scores)

def race(header, rows, label):
    """
    Compares 'random' search, 'greedy' (surrogate model), and 'big_team' (customer's current approach).
    Budget: 50 labels total.
    """
    inputs = [c for c in header if not (c.endswith(('-', '+')))]
    goals = [c for c in header if c.endswith(('-', '+'))]
    budget = 50
    queried = {}

    def get_label(idx):
        if idx not in queried:
            if len(queried) >= budget:
                raise Exception("Budget exceeded")
            queried[idx] = label(idx)
        return queried[idx]

    # Strategy 1: Random
    def strategy_random():
        idx = np.random.choice(len(rows))
        return idx, get_label(idx)

    # Strategy 2: Greedy (Surrogate model)
    def strategy_greedy():
        if len(queried) < 10: return strategy_random()
        df = pd.DataFrame([rows[i][:len(inputs)] + queried[i] for i in queried], columns=header)
        model = RandomForestRegressor(n_estimators=20).fit(df[inputs], [get_score(header, queried[i]) for i in queried])
        preds = model.predict([r[:len(inputs)] for r in rows])
        idx = int(np.argmax(preds))
        return idx, get_label(idx)

    # Strategy 3: Big Team (Customer's current approach: pick rows with highest Team Size)
    def strategy_big_team():
        # Sort rows by Team Size descending
        team_size_idx = header.index('Team Size')
        sorted_indices = np.argsort([-rows[i][team_size_idx] for i in range(len(rows))])
        # Pick the next best available
        for idx in sorted_indices:
            if idx not in queried:
                return idx, get_label(idx)
        return strategy_random()

    strategies = {"random": strategy_random, "greedy": strategy_greedy, "big_team": strategy_big_team}
    results = {name: {"best_score": -1, "best_idx": -1} for name in strategies}

    for i in range(budget):
        name = list(strategies.keys())[i % 3]
        idx, g = strategies[name]()
        score = get_score(header, g)
        if score > results[name]["best_score"]:
            results[name]["best_score"] = score
            results[name]["best_idx"] = idx

    winner = max(results, key=lambda n: results[n]["best_score"])
    return {"winner": winner, "row": results[winner]["best_idx"], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            data = [[float(val) for val in row] for row in reader]
        
        def label(i):
            return [data[i][j] for j, col in enumerate(header) if col.endswith(('-', '+'))]
        
        masked = [r[:len(header)-3] + ['?'] * 3 for r in data]
        
        res = race(header, masked, label)
        print("Customer Inquiry: Is your way of choosing better than our 'biggest teams' approach?")
        print(f"Race Results: The winner is the '{res['winner']}' strategy.")
        print(f"Best row found at index: {res['row']}")
        print(f"Strategies compared: {', '.join(res['tried'])}")
        if res['winner'] != 'big_team':
            print("Conclusion: Yes, data-driven optimization outperforms the 'biggest teams' heuristic.")
        else:
            print("Conclusion: Your current heuristic is performing optimally.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
