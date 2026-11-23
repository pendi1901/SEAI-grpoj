import ezr
import step01
import step07
import random

def race(header, rows, label):
    """
    Compares three strategies: random, acquire (from ezr), and a greedy search.
    The total budget of 50 labels is shared.
    """
    budget = 50
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(ezr.Tbl([header] + rows), rows[i]))

    # Strategy 2: Acquire (ezr's default)
    def strategy_acquire():
        tbl = ezr.Tbl([header] + rows)
        # We need to pass a wrapper that uses our shared get_label
        def oracle_wrapper(row):
            # Find index of row in original list
            for i, r in enumerate(rows):
                if r == row:
                    goals = get_label(i)
                    new_row = row[:]
                    goal_indices = [idx for idx, name in enumerate(header) 
                                    if name.endswith("-") or name.endswith("+")]
                    for g_idx, val in zip(goal_indices, goals):
                        new_row[g_idx] = val
                    return new_row
            return row
        
        best_rows = ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)
        best_row = min(best_rows, key=lambda r: ezr.ydist(tbl, r))
        for i, r in enumerate(rows):
            if r == best_row: return i
        return 0

    # Strategy 3: Greedy (using step01's logic)
    def strategy_greedy():
        indices = step01.remember(header, rows)[:budget // 3]
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(ezr.Tbl([header] + rows), rows[i]))

    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
    }

    results = {}
    for name, func in strategies.items():
        results[name] = func()

    # Determine winner based on ydist
    tbl = ezr.Tbl([header] + rows)
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))

    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    all_rows = list(rows_gen)

    def label(i):
        return [all_rows[i][idx] for idx, name in enumerate(header) 
                if name.endswith("-") or name.endswith("+")]

    result = race(header, all_rows, label)
    print(f"Race Results: Winner is '{result['winner']}' strategy.")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    exit(0)
