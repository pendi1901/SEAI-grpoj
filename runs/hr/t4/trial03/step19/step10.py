import csv
import random
from step01 import remember
from step07 import choose

def race(header, rows, label):
    """
    Compares three strategies for finding the best row (maximizing 'YearsAtCompany+').
    Budget: 50 labels total.
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+'))
    
    # Strategy 1: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        max_val = -float('inf')
        for i in indices:
            val = label(i)[0]
            if val > max_val:
                max_val = val
                best_idx = i
        return best_idx, max_val

    # Strategy 2: Top 5% (Heuristic)
    def strategy_heuristic(budget):
        # Use remember() logic to find candidates, then sample from them
        candidates = remember(header, rows)
        indices = random.sample(candidates, min(len(candidates), budget))
        best_idx = -1
        max_val = -float('inf')
        for i in indices:
            val = label(i)[0]
            if val > max_val:
                max_val = val
                best_idx = i
        return best_idx, max_val

    # Strategy 3: Early Bird (First 50)
    def strategy_first(budget):
        best_idx = -1
        max_val = -float('inf')
        for i in range(budget):
            val = label(i)[0]
            if val > max_val:
                max_val = val
                best_idx = i
        return best_idx, max_val

    # Allocate budget: 16 labels each (48 total)
    budget_per = 16
    
    res_random = strategy_random(budget_per)
    res_heuristic = strategy_heuristic(budget_per)
    res_first = strategy_first(budget_per)
    
    results = {
        "random": res_random[1],
        "heuristic": res_heuristic[1],
        "first": res_first[1]
    }
    
    best_strategy = max(results, key=results.get)
    best_row = res_random[0] if best_strategy == "random" else (res_heuristic[0] if best_strategy == "heuristic" else res_first[0])
    
    return {
        "winner": best_strategy,
        "row": best_row,
        "tried": ["random", "heuristic", "first"]
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

    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+'))
    true_goals = [row[goal_idx] for row in rows]
    
    # Mask rows
    for row in rows:
        row[goal_idx] = "?"
        
    def label(i):
        return [true_goals[i]]
    
    result = race(header, rows, label)
    
    print(f"Race complete. The winning strategy was: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    exit(0)
