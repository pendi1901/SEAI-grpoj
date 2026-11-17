import ezr


def race(header, rows, label):
    """Compare three strategies for finding the best row under a labelling budget."""
    
    # Identify goal columns (names ending in + or -)
    goals = [c for c in header if c[-1] in "+-"]
    
    def ydist_row(row):
        tbl = ezr.Tbl([header] + rows[:0])  # dummy, but we'll use the real tbl below
        return ezr.ydist(tbl, row)
    
    # Build a reference table with all rows (labels filled in where known)
    def build_tbl(labelled_indices):
        labelled_rows = [rows[i] if i not in labelled_indices else label(rows[i]) 
                         for i in range(len(rows))]
        return ezr.Tbl([header] + labelled_rows)
    
    # Strategy 1: Random sampling
    def strategy_random():
        budget = 50
        chosen = random.sample(range(len(rows)), min(budget, len(rows)))
        tbl = build_tbl(chosen)
        ranker_fn = ezr.ranker(tbl)
        scores = [ranker_fn(r) for r in rows]
        best_idx = min(range(len(scores)), key=lambda i: scores[i])
        return ("random", best_idx, chosen)
    
    # Strategy 2: Greedy - always pick the row closest to current best
    def strategy_greedy():
        budget = 50
        labelled = set()
        # Start with a random seed of 5 rows
        seed = random.sample(range(len(rows)), min(5, len(rows)))
        for i in seed:
            labelled.add(i)
        
        while len(labelled) < budget:
            tbl = build_tbl(list(labelled))
            ranker_fn = ezr.ranker(tbl)
            
            # Find the best labelled row's score
            scores_labelled = [ranker_fn(rows[i]) for i in labelled]
            best_score = min(scores_labelled)
            
            # Pick unlabelled row with lowest ydist (using current knowledge)
            best_unlabelled = None
            best_est = 1e30
            
            for i in range(len(rows)):
                if i not in labelled:
                    tbl_partial = ezr.Tbl([header] + [rows[i]])
                    d = ezr.ydist(tbl_partial, rows[i])
                    # Use a heuristic: compare to best labelled row
                    if len(labelled) > 0:
                        ref_tbl = build_tbl(list(labelled))
                        ref_ranker = ezr.ranker(ref_tbl)
                        est_score = ref_ranker(rows[i])
                        if est_score < best_est:
                            best_est = est_score
                            best_unlabelled = i
            
            if best_unlabelled is not None:
                labelled.add(best_unlabelled)
        
        tbl = build_tbl(list(labelled))
        ranker_fn = ezr.ranker(tbl)
        scores = [ranker_fn(r) for r in rows]
        best_idx = min(range(len(scores)), key=lambda i: scores[i])
        return ("greedy", best_idx, list(labelled))
    
    # Strategy 3: Random (already defined above as strategy_random)
    # Let's rename and create a proper third strategy
    
    # Actually, let me restructure this properly with three distinct strategies:
    # 1. random - pick rows at random
    # 2. greedy - iteratively pick best unlabelled row  
    # 3. stratified - divide into strata by input features, then sample within each
    
    def strategy_stratified():
        budget = 50
        
        # First, identify numeric input columns for stratification
        inputs = [c for i, c in enumerate(header) if not c[-1] in "+-" and c[0].isupper()]
        
        # Create strata based on first few numeric inputs
        n_strata = min(3, len(inputs))
        stratum_keys = []
        for s in range(n_strata):
            col_idx = inputs[s % len(inputs)]
            vals = [row[col_idx] if isinstance(row[col_idx], float) else 0.0 for row in rows]
            mid_val = sum(vals) / len(vals)
            stratum_keys.append(1 if v < mid_val else -1 for v in vals)
        
        # Assign each row to a stratum
        def get_stratum(row):
            key = tuple(stratum_keys[i % n_strata] for i in range(n_strata))
            return hash(key) % 3
        
        # Sample from each stratum
        strata = [set() for _ in range(3)]
        for i, row in enumerate(rows):
            s = get_stratum(row)
            strata[s].add(i)
        
        chosen = []
        for s in range(len(strata)):
            if len(chosen) >= budget:
                break
            available = list(strata[s])
            n_pick = min(17, len(available))  # ~50/3 per stratum
            picked = random.sample(available, n_pick)
            chosen.extend(picked)
        
        tbl = build_tbl(chosen)
        ranker_fn = ezr.ranker(tbl)
        scores = [ranker_fn(r) for r in rows]
        best_idx = min(range(len(scores)), key=lambda i: scores[i])
        return ("stratified", best_idx, chosen)
    
    # Run all three strategies
    results = []
    
    random_result = strategy_random()
    results.append(random_result)
    
    greedy_result = strategy_greedy()
    results.append(greedy_result)
    
    stratified_result = strategy_stratified()
    results.append(stratified_result)
    
    # Find the best result overall (lowest ydist for the chosen row)
    def get_ydist_for_row(idx):
        tbl_full = ezr.Tbl([header] + rows)
        return ezr.ydist(tbl_full, rows[idx])
    
    best_strategy_name = None
    best_idx = None
    best_score = 1e30
    
    for name, idx, chosen in results:
        score = get_ydist_for_row(idx)
        if score < best_score:
            best_score = score
            best_strategy_name = name
            best_idx = idx
    
    return {
        "winner": best_strategy_name,
        "row": best_idx,
        "tried": [r[0] for r in results]
    }


if __name__ == "__main__":
    import random as _random  # avoid shadowing
    
    with open("Health-ClosedIssues0000.train.csv", encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    header = list(lines[0].split(","))
    rows   = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    
    # Provide a label function that returns the row as-is (since goals are already filled)
    def label(row):
        return row
    
    result = race(header, rows, label)
    print(f"Winner: {result['winner']}, Row index: {result['row']}")
