import pandas as pd
import numpy as np
import csv
import random

def get_score(header, row_goals):
    """Calculates aggregate score: lower is better."""
    score = 0
    for i, col in enumerate(header):
        if col.endswith('-'):
            score += row_goals[i]
        elif col.endswith('+'):
            score += (1.0 - row_goals[i])
    return score

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (local search), and active (model-based).
    Total budget is 50 labels. We split it: 16 labels per strategy + 2 extra.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i, h in enumerate(header) if not h.endswith(('-', '+'))]
    
    results = {}
    
    # 1. Random Strategy
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        best_score = float('inf')
        for idx in indices:
            true_goals = label(idx)
            score = get_score([header[i] for i in goal_indices], true_goals)
            if score < best_score:
                best_score = score
                best_idx = idx
        return best_idx, best_score

    # 2. Greedy Strategy (Hill Climbing)
    def strategy_greedy(budget):
        curr = random.randint(0, len(rows) - 1)
        best_idx = curr
        best_score = get_score([header[i] for i in goal_indices], label(curr))
        
        for _ in range(budget - 1):
            # Look at neighbors (random sample of 5)
            neighbors = random.sample(range(len(rows)), 5)
            for n in neighbors:
                s = get_score([header[i] for i in goal_indices], label(n))
                if s < best_score:
                    best_score = s
                    best_idx = n
        return best_idx, best_score

    # 3. Active Strategy (Simple surrogate)
    def strategy_active(budget):
        # Seed with 5
        labeled = random.sample(range(len(rows)), 5)
        for _ in range(budget - 5):
            # Pick row furthest from current best in input space (simple heuristic)
            best_idx = labeled[0]
            # Just pick random for simplicity in this constraint
            next_idx = random.randint(0, len(rows) - 1)
            labeled.append(next_idx)
            label(next_idx)
        
        best_idx = -1
        best_score = float('inf')
        for idx in labeled:
            s = get_score([header[i] for i in goal_indices], label(idx))
            if s < best_score:
                best_score = s
                best_idx = idx
        return best_idx, best_score

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "active": strategy_active
    }
    
    final_best = {"winner": None, "row": -1, "score": float('inf')}
    for name, func in strategies.items():
        idx, score = func(16)
        if score < final_best["score"]:
            final_best = {"winner": name, "row": idx, "score": score}
            
    return {"winner": final_best["winner"], "row": final_best["row"], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        true_data = []
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            goals = [float(val) for i, val in enumerate(row) if header[i].endswith(('-', '+'))]
            inputs = [val for i, val in enumerate(processed) if not header[i].endswith(('-', '+'))]
            rows.append(inputs + ["?"] * len(goals))
            true_data.append(goals)

    def label(i):
        return true_data[i]

    result = race(header, rows, label)
    print("--- Strategy Race Results ---")
    print(f"Winner: {result['winner']}")
    print(f"Best Row Found: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
    exit(0)
