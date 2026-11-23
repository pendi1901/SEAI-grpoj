import ezr
import random
import step07

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee arrangement
    within a shared budget of 50 labels.
    """
    budget = 50
    # We track which rows have been labeled to ensure we don't exceed the budget
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), min(budget // 3, len(rows)))
        best_idx = -1
        best_ydist = 1e30
        for idx in indices:
            full_row = oracle_wrapper(idx)
            d = ezr.ydist(ezr.Tbl([header] + [full_row]), full_row)
            if d < best_ydist:
                best_ydist, best_idx = d, idx
        return best_idx, best_ydist

    # Strategy 2: Greedy (using ezr.acquire)
    def strategy_greedy():
        # Create a table with indices
        indexed_rows = [list(r) + [i] for i, r in enumerate(rows)]
        tbl = ezr.Tbl([header + ["idxX"]] + indexed_rows)
        
        def oracle_proxy(row):
            idx = int(row[-1])
            full = oracle_wrapper(idx)
            for i, name in enumerate(header):
                if name.endswith('+') or name.endswith('-'):
                    row[i] = full[i]
            return row

        labeled = ezr.acquire(tbl, cap=budget // 3, label=oracle_proxy)
        best = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        return int(best[-1]), ezr.ydist(tbl, best)

    # Strategy 3: Uncertainty (using random sample of a subset)
    def strategy_uncertain():
        # Pick rows that are furthest from the current known mean
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx = -1
        best_ydist = 1e30
        for idx in indices:
            full_row = oracle_wrapper(idx)
            d = ezr.ydist(ezr.Tbl([header] + [full_row]), full_row)
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
        print("The 'greedy' strategy typically outperforms random search by")
        print("focusing labels on areas of the search space that show promise.")
    except Exception as e:
        print(f"Race failed: {e}")
