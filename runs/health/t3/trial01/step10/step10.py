def race(header, rows, label):
    goals = ["MRE-", "ACC+", "PRED40+"]
    
    # Precompute best scores from step01 convention (lower is better)
    bests = {}
    for g in goals:
        vals = []
        for r in rows:
            v = float(r[header.index(g)])
            if g.endswith("-"):
                vals.append(v)
            else:
                vals.append(-v)
        bests[g] = min(vals)

    def score_row(goal_vals):
        s = 0.0
        for g in goals:
            v = goal_vals[g]
            if g.endswith("-"):
                s += (v - bests[g])
            else:
                s += (-v - bests[g])
        return s

    # Strategy 1: Random search - pick rows at random
    def strategy_random():
        import random
        n = len(rows)
        chosen = set()
        while len(chosen) < min(50, n):
            i = random.randint(0, n - 1)
            if i not in chosen:
                chosen.add(i)
        return list(chosen)

    # Strategy 2: Greedy search - pick best row first, then improve incrementally
    def strategy_greedy():
        scored = []
        for i in range(len(rows)):
            s = score_row(label(i))
            scored.append((i, s))
        scored.sort(key=lambda x: x[1])
        chosen = [pos for pos, _ in scored[:50]]
        return chosen

    # Strategy 3: Systematic search - try evenly spaced rows
    def strategy_systematic():
        n = len(rows)
        step = max(1, n // 50)
        chosen = list(range(step, n, step))
        if len(chosen) < 50:
            # Add first few to ensure we get enough
            for i in range(min(50 - len(chosen), n)):
                if i not in chosen:
                    chosen.append(i)
        return chosen

    # Run all strategies and collect results
    strategies = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "systematic": strategy_systematic()
    }

    # Evaluate each strategy's best row
    best_strategy = None
    best_row = None
    best_score = float('inf')
    
    for name, positions in strategies.items():
        for pos in positions:
            s = score_row(label(pos))
            if s < best_score:
                best_score = s
                best_strategy = name
                best_row = pos

    return {
        "winner": best_strategy,
        "row": best_row,
        "tried": list(strategies.keys())
    }


if __name__ == "__main__":
    import pandas as pd
    
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]

    # Mask goal cells with "?"
    for row in rows:
        for g in ["MRE-", "ACC+", "PRED40+"]:
            idx = header.index(g)
            row[idx] = "?"

    result = race(header, rows, lambda i: {g: float(rows[i][header.index(g)]) for g in ["MRE-", "ACC+", "PRED40+"]})

    print(f"Winner: {result['winner']}, Best row: {result['row']}, Tried: {result['tried']}")
