import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee record using a 
    shared budget of 50 labels.
    """
    # Shared budget management
    labeled_cache = {}
    
    def get_label(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(rows[idx])
        return labeled_cache[idx]

    # Strategies
    def strategy_random(tbl, budget):
        indices = random.sample(range(len(rows)), budget)
        for i in indices: get_label(i)
        return min(labeled_cache.keys(), key=lambda i: ezr.ydist(tbl, labeled_cache[i]))

    def strategy_active(tbl, budget):
        # Start with a few random
        for i in random.sample(range(len(rows)), 5): get_label(i)
        # Iteratively pick best
        while len(labeled_cache) < budget:
            lab_rows = [labeled_cache[i] for i in labeled_cache]
            lab_tbl = ezr.clone(tbl, lab_rows)
            rank_fn = ezr.ranker(lab_tbl)
            unlabeled = [i for i in range(len(rows)) if i not in labeled_cache]
            best_idx = min(unlabeled, key=lambda i: rank_fn(rows[i]))
            get_label(best_idx)
        return min(labeled_cache.keys(), key=lambda i: ezr.ydist(tbl, labeled_cache[i]))

    def strategy_greedy(tbl, budget):
        # Greedy: pick rows that are furthest from current bests
        for i in random.sample(range(len(rows)), 5): get_label(i)
        while len(labeled_cache) < budget:
            lab_rows = [labeled_cache[i] for i in labeled_cache]
            lab_tbl = ezr.clone(tbl, lab_rows)
            # Find row furthest from current best
            best_known = min(lab_rows, key=lambda r: ezr.ydist(lab_tbl, r))
            unlabeled = [i for i in range(len(rows)) if i not in labeled_cache]
            best_idx = max(unlabeled, key=lambda i: ezr.xdist(tbl, rows[i], best_known))
            get_label(best_idx)
        return min(labeled_cache.keys(), key=lambda i: ezr.ydist(tbl, labeled_cache[i]))

    # Run race
    tbl = ezr.Tbl([header] + rows)
    results = {}
    
    # Reset cache for each strategy to ensure fair budget usage
    strategies = {"random": strategy_random, "active": strategy_active, "greedy": strategy_greedy}
    for name, func in strategies.items():
        labeled_cache = {}
        best_idx = func(tbl, 16) # 16 * 3 = 48 labels total
        results[name] = (best_idx, ezr.ydist(tbl, labeled_cache[best_idx]))

    winner = min(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    def label(row):
        return row

    result = race(header, rows, label)
    
    print("Race Results: Which strategy finds the best employee record?")
    print("-" * 60)
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    print("-" * 60)
    print("The 'active' strategy typically outperforms random search by")
    print("focusing labels on the most promising regions of the data.")
