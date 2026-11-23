import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy, and acquisition.
    Budget: 50 labels total.
    """
    budget = 50
    labeled_cache = {}  # {index: row_with_goals}
    
    def get_row(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            row = list(rows[i])
            goals = label(i)
            goal_indices = [j for j, name in enumerate(header) if name.endswith(('-', '+'))]
            for idx, val in zip(goal_indices, goals):
                row[idx] = val
            labeled_cache[i] = row
        return labeled_cache[i]

    # Strategies
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        return [get_row(i) for i in indices]

    def strategy_greedy():
        indices = random.sample(range(len(rows)), budget // 3)
        return [get_row(i) for i in indices]

    def strategy_acquire():
        # Use a small subset of the budget for the acquire function
        start_indices = random.sample(range(len(rows)), 5)
        initial_rows = [get_row(i) for i in start_indices]
        tbl = ezr.Tbl([header] + initial_rows)
        
        def oracle_wrapper(row):
            # Find index of this row in original rows
            for i, r in enumerate(rows):
                if r is row: return get_row(i)
            return row
            
        return ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)

    # Run strategies
    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "acquire": strategy_acquire
    }
    
    results = {name: func() for name, func in strategies.items()}

    # Evaluate: Find the best row across all labeled rows
    all_labeled = list(labeled_cache.values())
    ref_tbl = ezr.Tbl([header] + all_labeled)
    
    best_ydist = 1e30
    winner = None
    best_idx = -1

    for name, found_rows in results.items():
        for r in found_rows:
            d = ezr.ydist(ref_tbl, r)
            if d < best_ydist:
                best_ydist = d
                winner = name
                # Find original index
                for i, original_row in enumerate(rows):
                    if all(original_row[j] == r[j] for j in range(len(r)) if not header[j].endswith(('-', '+'))):
                        best_idx = i
                        break

    return {"winner": winner, "row": best_idx, "tried": list(results.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Keep a copy of full data for the label function
    full_data = [list(r) for r in rows]
    
    def label(i):
        return [full_data[i][idx] for idx in goal_indices]
    
    # Mask rows for the race
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    result = race(header, rows, label)
    print(f"Race Results: The winner is '{result['winner']}' strategy.")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    exit(0)
