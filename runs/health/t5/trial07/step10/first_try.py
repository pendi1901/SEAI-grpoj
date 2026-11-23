import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best configuration:
    1. 'random': Random sampling.
    2. 'acquire': The active learning strategy from ezr.
    3. 'greedy': A simple greedy search starting from a random point.
    """
    budget = 50
    labeled = {}

    def oracle_wrapper(idx):
        if idx not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[idx] = label(idx)
        return labeled[idx]

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))

    # Strategy 2: Acquire (Active Learning)
    def strategy_acquire():
        # We use a subset of the budget for the acquire function
        # The acquire function handles its own internal labeling
        subset_rows = ezr.acquire(tbl, cap=budget // 3, label=lambda r: oracle_wrapper(rows.index(r)))
        best_row = min(subset_rows, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Strategy 3: Greedy (Hill Climbing)
    def strategy_greedy():
        curr = random.choice(range(len(rows)))
        for _ in range(budget // 3):
            neighbors = random.sample(range(len(rows)), 5)
            best_n = min(neighbors, key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))
            if ezr.ydist(tbl, oracle_wrapper(best_n)) < ezr.ydist(tbl, oracle_wrapper(curr)):
                curr = best_n
        return curr

    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
    }

    results = {}
    for name, func in strategies.items():
        results[name] = func()

    # Determine winner: lowest ydist
    winner = min(results, key=lambda n: ezr.ydist(tbl, oracle_wrapper(results[n])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Mask goals
    masked_rows = []
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(idx):
        return rows[idx]
    
    random.seed(1234567891)
    result = race(header, masked_rows, label)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
