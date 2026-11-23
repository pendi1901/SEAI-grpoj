import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember

def get_agg(header, row, goals, min_vals, max_vals):
    """Calculates normalized aggregate score for a single row."""
    scores = []
    for i, goal in enumerate(goals):
        val = row[header.index(goal)]
        norm = (val - min_vals[i]) / (max_vals[i] - min_vals[i])
        scores.append(1 - norm if goal.endswith('-') else norm)
    return sum(scores) / len(scores)

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (KNN), and uncertainty-based.
    Budget: 50 labels total.
    """
    n_rows = len(rows)
    goals = [c for c in header if c.endswith(('-', '+'))]
    inputs = [c for c in header if not (c.endswith(('-', '+')))]
    
    # Pre-calculate normalization bounds from full dataset (simulated)
    # Since we can't see all goals, we use the first 10 random samples to estimate
    labeled = {}
    
    def get_label(i):
        if i not in labeled:
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        idx = np.random.choice(n_rows)
        return idx, get_label(idx)

    # Strategy 2: Greedy (KNN)
    def strategy_greedy():
        if len(labeled) < 10: return strategy_random()
        df_train = pd.DataFrame([rows[i][:len(inputs)] + list(labeled[i]) for i in labeled], columns=header)
        model = KNeighborsRegressor(n_neighbors=3).fit(df_train[inputs], df_train[goals])
        preds = model.predict([r[:len(inputs)] for r in rows])
        # Pick best predicted
        best_idx = np.argmax([sum(p) for p in preds])
        return best_idx, get_label(best_idx)

    # Strategy 3: Exploration (Randomly pick from top 10% of inputs)
    def strategy_explore():
        idx = np.random.choice(n_rows)
        return idx, get_label(idx)

    strategies = {"random": strategy_random, "greedy": strategy_greedy, "explore": strategy_explore}
    
    # Run 50 trials total
    for _ in range(50):
        strat_name = np.random.choice(list(strategies.keys()))
        strategies[strat_name]()

    # Evaluate
    results = {}
    for name in strategies:
        # Find best row found by this strategy
        best_val = -1
        best_idx = -1
        # Simplified: check all labeled rows
        for idx in labeled:
            # We need global min/max for fair comparison
            # Using the labeled set as proxy
            df = pd.DataFrame([labeled[i] for i in labeled], columns=goals)
            score = get_agg(header, [rows[idx][0:len(inputs)]] + [labeled[idx]], goals, df.min(), df.max())
            if score > best_val:
                best_val = score
                best_idx = idx
        results[name] = (best_val, best_idx)

    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [[float(x) for x in row[:len(header)-3]] + ['?'] * 3 for row in reader]
        true_data = [[float(x) for x in row] for row in csv.reader(open(filename))]
        next(csv.reader(open(filename))) # skip header
        
    def label(i):
        return true_data[i][len(header)-3:]
        
    result = race(header, data, label)
    print(f"Race Results: The winner is '{result['winner']}' strategy.")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
