import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, big_teams, and acquisition.
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

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        return [get_row(i) for i in indices]

    # Strategy 2: Big Teams (Customer's current approach)
    def strategy_big_teams():
        team_idx = header.index("Team Size")
        # Sort by team size descending and pick the largest
        indexed = sorted(enumerate(rows), key=lambda x: x[1][team_idx], reverse=True)
        indices = [x[0] for x in indexed[:budget // 3]]
        return [get_row(i) for i in indices]

    # Strategy 3: Acquisition (Intelligent search)
    def strategy_acquire():
        start_indices = random.sample(range(len(rows)), 5)
        initial_rows = [get_row(i) for i in start_indices]
        tbl = ezr.Tbl([header] + initial_rows)
        
        def oracle_wrapper(row):
            for i, r in enumerate(rows):
                if r is row: return get_row(i)
            return row
            
        return ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)

    strategies = {
        "random": strategy_random,
        "big_teams": strategy_big_teams,
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
                for i, original_row in enumerate(rows):
                    if all(original_row[j] == r[j] for j in range(len(r)) if not header[j].endswith(('-', '+'))):
                        best_idx = i
                        break

    return {"winner": winner, "row": best_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    full_data = [list(r) for r in rows]
    
    def label(i):
        return [full_data[i][idx] for idx in goal_indices]
    
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    result = race(header, rows, label)
    
    print("Optimization Strategy Comparison:")
    print(f"The winning strategy is: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    if result['winner'] != "big_teams":
        print("\nConclusion: Your current 'big teams' approach is outperformed by smarter search strategies.")
    else:
        print("\nConclusion: Your 'big teams' approach is currently optimal.")
    exit(0)
