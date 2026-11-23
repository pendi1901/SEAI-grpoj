import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and tree-based.
    Budget: 50 labels total.
    """
    budget = 50
    used_indices = set()

    def get_label(i):
        if i not in used_indices:
            if len(used_indices) >= budget:
                raise Exception("Budget exceeded")
            used_indices.add(i)
        return label(i)

    def run_strategy(name, strategy_func):
        # Create a fresh copy of rows for this strategy
        temp_rows = [list(r) for r in rows]
        # We must use the original data indices to label
        # Strategy logic:
        if name == "random":
            indices = random.sample(range(len(temp_rows)), budget // 3)
            for i in indices:
                goals = get_label(i)
                for j, val in enumerate(goals):
                    temp_rows[i][9 + j] = val
        elif name == "greedy":
            curr = random.randint(0, len(temp_rows) - 1)
            for _ in range(budget // 3):
                goals = get_label(curr)
                for j, val in enumerate(goals):
                    temp_rows[curr][9 + j] = val
                # Find nearest unlabelled
                best_d, best_i = 1e30, -1
                for i in range(len(temp_rows)):
                    if i not in used_indices:
                        d = ezr.xdist(ezr.Tbl([header] + temp_rows), temp_rows[curr], temp_rows[i])
                        if d < best_d:
                            best_d, best_i = d, i
                if best_i == -1: break
                curr = best_i
        elif name == "tree":
            # Use a wrapper for acquire
            tbl = ezr.Tbl([header] + temp_rows)
            def oracle_wrapper(r):
                # Find index of row in temp_rows
                idx = temp_rows.index(r)
                goals = get_label(idx)
                for j, val in enumerate(goals):
                    r[9 + j] = val
                return r
            ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)
        
        # Evaluate
        best_ydist = 1e30
        best_idx = -1
        tbl = ezr.Tbl([header] + temp_rows)
        for i, r in enumerate(temp_rows):
            if "?" not in r[9:]:
                d = ezr.ydist(tbl, r)
                if d < best_ydist:
                    best_ydist, best_idx = d, i
        return best_ydist, best_idx

    strategies = ["random", "greedy", "tree"]
    results = {}
    for name in strategies:
        # Reset used_indices for each strategy to ensure fair budget usage per strategy
        # but the rule says budget is shared. We will split the 50 budget.
        used_indices = set() 
        results[name] = run_strategy(name, None)

    winner = min(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": strategies}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    for r in rows:
        r[9] = r[10] = r[11] = "?"
        
    full_data = list(ezr.csv(filename))
    full_rows = full_data[1:]
    
    def label_func(i):
        return [full_rows[i][9], full_rows[i][10], full_rows[i][11]]
    
    res = race(header, rows, label_func)
    print(f"Race Results: The winner is '{res['winner']}' strategy.")
    print(f"Best row found at index: {res['row']}")
    print(f"Strategies compared: {', '.join(res['tried'])}")
    exit(0)
