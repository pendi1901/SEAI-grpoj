import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (based on tree ranker), 
    and the acquire strategy.
    """
    # Budget management
    budget = 50
    labeled = {}

    def oracle_wrapper(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            # Get true goals
            goals = label(i)
            # Update the row in the list with its true goals
            for j, val in enumerate(goals):
                rows[i][j] = val
            labeled[i] = goals
        return rows[i]

    # Prepare data: TBL needs rows with goals filled to calculate ydist correctly.
    # We create a copy of rows to avoid mutating the original input if needed,
    # but here we need to update the rows as we label them.
    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        for i in indices:
            oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Greedy (Tree-based)
    def strategy_greedy():
        # Train on initial random sample
        train_indices = random.sample(range(len(rows)), 10)
        for i in train_indices: oracle_wrapper(i)
        
        # Build ranker on currently labeled data
        lab_rows = [rows[i] for i in train_indices]
        lab_tbl = ezr.Tbl([header] + lab_rows)
        ranker = ezr.ranker(lab_tbl)
        
        # Pick best from remaining
        candidates = [i for i in range(len(rows)) if i not in labeled]
        best_i = min(candidates, key=lambda i: ranker(rows[i]))
        oracle_wrapper(best_i)
        return best_i

    # Strategy 3: Acquire (ezr's built-in)
    def strategy_acquire():
        # Acquire needs a TBL. We use the existing tbl.
        # We need to pass a label function that updates our shared state.
        def oracle_proxy(r):
            for i, orig in enumerate(rows):
                if r is orig:
                    return oracle_wrapper(i)
            return r
            
        best_rows = ezr.acquire(tbl, cap=16, label=oracle_proxy)
        best_row = min(best_rows, key=lambda r: ezr.ydist(tbl, r))
        for i, r in enumerate(rows):
            if r is best_row: return i
        return 0

    # Run race
    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "acquire": strategy_acquire()
    }
    
    # Determine winner (lowest ydist)
    winner = min(results, key=lambda k: ezr.ydist(tbl, rows[results[k]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "greedy", "acquire"]
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Keep a copy of the original goals to simulate the oracle
    original_goals = [row[:3] for row in all_rows]
    
    # Mask the rows for the race
    for row in all_rows:
        for i in range(3):
            row[i] = "?"
    
    def label_func(i):
        return original_goals[i]
    
    # Run the race
    outcome = race(header, all_rows, label_func)
    
    print("Race Results:")
    print(f"Winner: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
    
    exit(0)
