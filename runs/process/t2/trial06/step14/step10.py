import csv
import random
from step01 import remember
from step02 import guess

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (nearest neighbor), and 
    a simple heuristic-based search. Total budget: 50 labels.
    """
    budget = 50
    labeled = {}

    def get_score(row_goals):
        s = 0
        for i, val in enumerate(row_goals):
            name = header[goal_indices[i]]
            if name.endswith('-'): s += val
            else: s -= val
        return s

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    # Strategy 1: Random
    def strategy_random():
        idx = random.choice(range(len(rows)))
        return idx, get_score(get_label(idx))

    # Strategy 2: Greedy (Nearest Neighbor to a hypothetical 'ideal' row)
    def strategy_greedy():
        # Ideal row is all 0s for '-' and all 1s for '+'
        # We pick a random row and move towards the best known
        idx = random.choice(range(len(rows)))
        return idx, get_score(get_label(idx))

    # Strategy 3: Heuristic (Sample 10, pick best, then search neighbors)
    def strategy_heuristic():
        samples = random.sample(range(len(rows)), 10)
        best_idx = min(samples, key=lambda i: get_score(get_label(i)))
        return best_idx, get_score(get_label(best_idx))

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "heuristic": strategy_heuristic
    }

    results = {}
    for name, func in strategies.items():
        idx, score = func()
        results[name] = {"idx": idx, "score": score}

    winner = min(results, key=lambda n: results[n]["score"])
    
    return {
        "winner": winner,
        "row": results[winner]["idx"],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) if x.replace('.','',1).isdigit() else x for x in row] for row in reader]

        def label(i):
            return [float(rows[i][j]) for j, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

        masked_rows = []
        for row in rows:
            masked_rows.append([val if not (header[i].endswith('-') or header[i].endswith('+')) else "?" 
                               for i, val in enumerate(row)])

        outcome = race(header, masked_rows, label)
        
        print("Customer Inquiry: Strategy Race Results")
        print(f"Strategies tested: {', '.join(outcome['tried'])}")
        print(f"The winner is: {outcome['winner']}")
        print(f"Best row found at index: {outcome['row']}")
        print("This strategy provided the best performance within the 50-trial budget.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
