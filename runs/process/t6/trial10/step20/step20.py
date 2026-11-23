import ezr
import step01
import step10
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks rows at random.
    2. 'big_teams': The customer's current strategy (picks rows with largest Team Size).
    3. 'acquire': The ezr.acquire strategy.
    """
    budget = 50
    labeled = {}
    team_size_idx = 8  # 'Team Size' index

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[i] = label(i)
        return labeled[i]

    # Setup full table for distance calculations
    rows_with_labels = [r[:] for r in rows]
    goal_indices = [i for i, name in enumerate(header) if name.endswith("-") or name.endswith("+")]
    
    def update_row(i):
        vals = get_label(i)
        if vals:
            for g_idx, val in zip(goal_indices, vals):
                rows_with_labels[i][g_idx] = val

    tbl_full = ezr.Tbl([header] + rows_with_labels)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: update_row(i)
        return min(indices, key=lambda i: ezr.ydist(tbl_full, rows_with_labels[i]))

    # Strategy 2: Big Teams (Customer's current approach)
    def strategy_big_teams():
        # Sort by Team Size descending and pick top ones
        indices = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        subset = indices[:budget // 3]
        for i in subset: update_row(i)
        return min(subset, key=lambda i: ezr.ydist(tbl_full, rows_with_labels[i]))

    # Strategy 3: Acquire
    def strategy_acquire():
        subset_size = min(len(rows), 200)
        subset_indices = random.sample(range(len(rows)), subset_size)
        subset_rows = [rows[i] for i in subset_indices]
        
        def oracle_wrapper(row):
            for i in subset_indices:
                if rows[i] == row:
                    update_row(i)
                    return rows_with_labels[i]
            return row
        
        tbl_sub = ezr.Tbl([header] + subset_rows)
        best_rows = ezr.acquire(tbl_sub, cap=budget // 3, label=oracle_wrapper)
        best_row = min(best_rows, key=lambda r: ezr.ydist(tbl_full, r))
        for i in range(len(rows)):
            if rows_with_labels[i] == best_row: return i
        return 0

    strategies = {
        "random": strategy_random,
        "big_teams": strategy_big_teams,
        "acquire": strategy_acquire
    }

    results = {}
    for name, func in strategies.items():
        results[name] = func()

    winner = min(results, key=lambda name: ezr.ydist(tbl_full, rows_with_labels[results[name]]))

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
    print(f"Race Results: The '{result['winner']}' strategy found the best configuration.")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    if result['winner'] == 'acquire':
        print("\nConclusion: Our 'acquire' strategy outperforms the 'big_teams' approach.")
    else:
        print("\nConclusion: The 'big_teams' approach is competitive, but consider testing 'acquire'.")
    exit(0)
