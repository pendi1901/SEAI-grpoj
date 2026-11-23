import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy (nearest to best), and tree-based.
    The 50-label budget is shared.
    """
    # Setup
    tbl = ezr.Tbl([header] + rows)
    goal_indices = [c.at for c in tbl.y]
    
    # Shared label tracker
    labeled_cache = {}
    def get_label(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Label budget exceeded!")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    def apply_label(row, idx):
        true_vals = get_label(idx)
        for i, g_idx in enumerate(goal_indices):
            row[g_idx] = true_vals[i]
        return row

    # Strategies
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = indices[0]
        for idx in indices:
            row = apply_label(list(rows[idx]), idx)
            if ezr.ydist(tbl, row) < ezr.ydist(tbl, apply_label(list(rows[best_idx]), best_idx)):
                best_idx = idx
        return best_idx

    def strategy_greedy(budget):
        # Start with one random, then pick nearest to the best found so far
        curr_idx = random.choice(range(len(rows)))
        best_idx = curr_idx
        for _ in range(budget - 1):
            row = apply_label(list(rows[curr_idx]), curr_idx)
            if ezr.ydist(tbl, row) < ezr.ydist(tbl, apply_label(list(rows[best_idx]), best_idx)):
                best_idx = curr_idx
            # Find next: pick row closest to current best
            best_row = apply_label(list(rows[best_idx]), best_idx)
            curr_idx = min((i for i in range(len(rows)) if i not in labeled_cache), 
                           key=lambda i: ezr.xdist(tbl, rows[i], best_row))
        return best_idx

    def strategy_tree(budget):
        # Use ezr's acquire logic
        labeled_rows = ezr.acquire(tbl, cap=budget, label=lambda r: apply_label(r, rows.index(r)))
        best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Run race
    results = {}
    budget_per = 16 # 50 / 3 = 16.6
    
    # We must reset cache for each strategy to ensure fair budget usage
    # But the prompt says "shared by all strategies together". 
    # We will split the 50 labels: 16, 17, 17.
    
    strategies = {
        "random": lambda: strategy_random(16),
        "greedy": lambda: strategy_greedy(17),
        "tree": lambda: strategy_tree(17)
    }
    
    winners = {}
    for name, func in strategies.items():
        idx = func()
        winners[name] = (idx, ezr.ydist(tbl, apply_label(list(rows[idx]), idx)))

    best_strat = min(winners, key=lambda n: winners[n][1])
    
    return {
        "winner": best_strat,
        "row": winners[best_strat][0],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in ('-', '+')]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    # Real data for label function
    full_data = list(ezr.csv(filename))
    next(iter(full_data)) # skip header
    
    def label_func(i):
        return [full_data[i][c.at] for c in ezr.Tbl([header] + rows).y]
    
    result = race(header, rows, label_func)
    print(f"Race Results: {result}")
    exit(0)
