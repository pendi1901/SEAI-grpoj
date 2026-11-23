import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee arrangement
    within a shared budget of 50 labels.
    """
    budget = 50
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # Helper to calculate ydist for a row given the full header
    def get_ydist(row):
        # Create a dummy table to use ydist
        tbl = ezr.Tbl([header, row])
        return ezr.ydist(tbl, row)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx = -1
        best_ydist = 1e30
        for idx in indices:
            full_row = oracle_wrapper(idx)
            d = get_ydist(full_row)
            if d < best_ydist:
                best_ydist, best_idx = d, idx
        return best_idx, best_ydist

    # Strategy 2: Greedy (using ezr.acquire)
    def strategy_greedy():
        indexed_rows = [list(r) + [i] for i, r in enumerate(rows)]
        tbl = ezr.Tbl([header + ["idxX"]] + indexed_rows)
        
        def oracle_proxy(row):
            idx = int(row[-1])
            full = oracle_wrapper(idx)
            # Update row with real values
            for i in range(len(header)):
                row[i] = full[i]
            return row

        labeled = ezr.acquire(tbl, cap=budget // 3, label=oracle_proxy)
        best = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        return int(best[-1]), ezr.ydist(tbl, best)

    # Strategy 3: Uncertainty (using random sample of a subset)
    def strategy_uncertain():
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx = -1
        best_ydist = 1e30
        for idx in indices:
            full_row = oracle_wrapper(idx)
            d = get_ydist(full_row)
            if d < best_ydist:
                best_ydist, best_idx = d, idx
        return best_idx, best_ydist

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "uncertain": strategy_uncertain()
    }

    winner = min(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    def real_label(i):
        return rows[i]

    try:
        outcome = race(header, rows, real_label)
        print("Strategy Race Results:")
        print("-" * 30)
        print(f"Winner: {outcome['winner']}")
        print(f"Best Row Index Found: {outcome['row']}")
        print(f"Strategies Tried: {', '.join(outcome['tried'])}")
        print("-" * 30)
    except Exception as e:
        print(f"Race failed: {e}")
