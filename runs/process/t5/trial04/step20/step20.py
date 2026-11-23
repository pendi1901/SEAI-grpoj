import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies:
    1. 'random': Randomly samples rows.
    2. 'big_teams': Always picks rows with the largest Team Size.
    3. 'tree': Uses ezr.acquire to intelligently sample the space.
    """
    tbl = ezr.Tbl([header] + rows)
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    team_idx = header.index("Team Size")
    
    # Shared budget tracker
    labeled_cache = {}
    def get_row_with_goals(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
        
        row = list(rows[i])
        goals = labeled_cache[i]
        for idx, val in zip(goal_indices, goals):
            row[idx] = val
        return row

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx = indices[0]
        for i in indices:
            if ezr.ydist(tbl, get_row_with_goals(i)) < ezr.ydist(tbl, get_row_with_goals(best_idx)):
                best_idx = i
        return best_idx

    # Strategy 2: Big Teams (Customer's current approach)
    def strategy_big_teams():
        # Sort by Team Size descending and pick the top 16
        sorted_by_team = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
        indices = sorted_by_team[:16]
        best_idx = indices[0]
        for i in indices:
            if ezr.ydist(tbl, get_row_with_goals(i)) < ezr.ydist(tbl, get_row_with_goals(best_idx)):
                best_idx = i
        return best_idx

    # Strategy 3: Tree-based (ezr.acquire)
    def strategy_tree():
        def oracle_wrapper(row):
            for i, r in enumerate(rows):
                if r == row:
                    return get_row_with_goals(i)
            return row
        
        labeled_rows = ezr.acquire(tbl, cap=18, label=oracle_wrapper)
        best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
        for i, r in enumerate(rows):
            if r == best_row: return i
        return 0

    results = {
        "random": strategy_random(),
        "big_teams": strategy_big_teams(),
        "tree": strategy_tree()
    }

    # Determine winner (lowest ydist)
    best_strategy = min(results, key=lambda s: ezr.ydist(tbl, get_row_with_goals(results[s])))
    
    return {
        "winner": best_strategy,
        "row": results[best_strategy],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    all_rows = list(data_gen)
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return [all_rows[i][idx] for idx in goal_indices]
        
    result = race(header, masked_rows, label_func)
    
    print("Strategy Comparison: Is 'Biggest Team' the best approach?")
    print("-" * 60)
    print(f"Winner: {result['winner']}")
    print(f"Best setup found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    print("-" * 60)
    if result['winner'] == "big_teams":
        print("Conclusion: Your current strategy of using the biggest teams is optimal.")
    else:
        print("Conclusion: Our intelligent search found better setups than simply maximizing team size.")
    exit(0)
