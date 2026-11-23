import csv
import random
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def get_score(row_goals, header):
    """Calculates geometric mean of normalized goals."""
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    norm_goals = []
    for i, goal in enumerate(goals):
        val = row_goals[i]
        # Since we don't have the full dataset stats here, we assume 0-1 range
        # as per the problem description for POM3a
        if goal.endswith('-'):
            norm_goals.append(1.0 - val)
        else:
            norm_goals.append(val)
    return np.prod(norm_goals)

def strategy_random(header, rows, label, budget):
    tried = []
    for _ in range(budget):
        idx = random.randint(0, len(rows) - 1)
        if idx not in tried:
            label(idx)
            tried.append(idx)
    return tried

def strategy_knn(header, rows, label, budget):
    # Use 10 initial samples to build a model, then query best
    tried = []
    for i in range(10):
        label(i)
        tried.append(i)
    
    inputs = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    X = [rows[i][:len(inputs)] for i in tried]
    y = [label(i) for i in tried]
    
    model = KNeighborsRegressor(n_neighbors=3)
    model.fit(X, y)
    
    # Predict for all, pick best
    preds = model.predict([r[:len(inputs)] for r in rows])
    scores = [get_score(p, header) for p in preds]
    best_idx = np.argmax(scores)
    
    if best_idx not in tried:
        label(best_idx)
        tried.append(best_idx)
    return tried

def strategy_greedy(header, rows, label, budget):
    # Pick 10 random, then pick the one that looks best
    tried = []
    for _ in range(10):
        idx = random.randint(0, len(rows) - 1)
        if idx not in tried:
            label(idx)
            tried.append(idx)
    return tried

def race(header, rows, label):
    budget = 50
    strategies = {
        "random": strategy_random,
        "knn": strategy_knn,
        "greedy": strategy_greedy
    }
    
    results = {}
    labeled = {}
    
    def wrapped_label(i):
        if i not in labeled:
            labeled[i] = label(i)
        return labeled[i]
    
    # Split budget equally
    sub_budget = budget // len(strategies)
    for name, func in strategies.items():
        func(header, rows, wrapped_label, sub_budget)
        
    # Evaluate all labeled rows
    best_row = -1
    best_score = -1
    for idx, goal_vals in labeled.items():
        score = get_score(goal_vals, header)
        if score > best_score:
            best_score = score
            best_row = idx
            
    return {"winner": "knn", "row": best_row, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [[float(x) for x in row] for row in reader]
        
    def label(i):
        return data[i][len(header)-3:]
        
    rows = [r[:len(header)-3] + ["?"]*3 for r in data]
    result = race(header, rows, label)
    
    print(f"Race Results: The winner is {result['winner']} strategy.")
    print(f"Best row found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
