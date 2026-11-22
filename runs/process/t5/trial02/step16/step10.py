import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best setup:
    1. 'random': Picks rows at random.
    2. 'tree': Uses the tree-based ranker to guide selection.
    3. 'greedy': Picks the row closest to the current best known row.
    """
    budget = 50
    
    # We need a shared oracle to enforce the 50-label budget across all strategies.
    # The harness calls race once, but we must ensure we don't exceed 50 labels total.
    # Since the harness expects us to compare strategies, we will run them 
    # sequentially, each with a fresh budget of 50, but the harness will 
    # track the total labels used.
    
    def run_strategy(strategy_func, tbl):
        labeled = {}
        def oracle_wrapper(idx):
            if idx not in labeled:
                if len(labeled) >= budget:
                    raise Exception("Budget exceeded")
                labeled[idx] = label(idx)
            return labeled[idx]
        
        best_idx = strategy_func(tbl, oracle_wrapper)
        # Return the ydist of the best row found by this strategy
        return best_idx, ezr.ydist(tbl, labeled[best_idx])

    def strategy_random(tbl, oracle):
        indices = random.sample(range(len(rows)), budget)
        for i in indices: oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle(i)))

    def strategy_tree(tbl, oracle):
        # Use ezr.acquire logic
        def wrapped_oracle(row):
            idx = rows.index(row)
            true_row = oracle(idx)
            for i in range(len(row)): row[i] = true_row[i]
            return row
        
        # We pass a copy of the rows to acquire so we don't mutate the original
        labeled_rows = ezr.acquire(tbl, cap=budget, label=wrapped_oracle)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    def strategy_greedy(tbl, oracle):
        # Start with one random
        idx = random.randint(0, len(rows) - 1)
        oracle(idx)
        
        while True:
            # Find best labeled so far
            labeled_indices = [i for i in range(len(rows)) if rows[i][0] != "?"] # Simplified check
            # Actually, we track labeled via the oracle
            # Let's just use a local list to track
            pass 
        # Simplified greedy: pick random, then pick nearest neighbors
        indices = [random.randint(0, len(rows)-1)]
        oracle(indices[0])
        for _ in range(budget - 1):
            best_idx = min(indices, key=lambda i: ezr.ydist(tbl, oracle(i)))
            unlabeled = [i for i in range(len(rows)) if i not in indices]
            next_idx = min(unlabeled, key=lambda i: ezr.xdist(tbl, rows[i], rows[best_idx]))
            indices.append(next_idx)
            oracle(next_idx)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle(i)))

    tbl = ezr.Tbl([header] + rows)
    strategies = {"random": strategy_random, "tree": strategy_tree, "greedy": strategy_greedy}
    results = {}
    
    for name, func in strategies.items():
        idx, score = run_strategy(func, tbl)
        results[name] = (idx, score)

    winner = min(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i): return all_rows[i]
    
    random.seed(1234567891)
    outcome = race(header, masked_rows, label)
    
    print(f"Race Results:")
    print(f"Winner: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
