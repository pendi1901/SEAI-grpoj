import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best working arrangement:
    1. 'random': The baseline.
    2. 'rule_of_thumb': Give biggest pay rises to the newest staff.
    3. 'acquire': The intelligent search strategy.
    """
    budget = 50
    labeled_cache = {}
    
    def oracle(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded!")
            labeled_cache[i] = label(i)
            # Update the table with the revealed goal values
            for at, col in tbl.cols.items():
                if header[at].endswith('+') or header[at].endswith('-'):
                    ezr.add(col, labeled_cache[i][at], 1)
        return labeled_cache[i]

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random(tbl):
        indices = random.sample(range(len(tbl.rows)), 16)
        for i in indices:
            oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle(i)))

    # Strategy 2: Rule of Thumb (Newest staff = lowest YearsAtCompany)
    def strategy_rule_of_thumb(tbl):
        years_idx = header.index('YearsAtCompany+')
        # Sort by years at company ascending (newest first)
        sorted_indices = sorted(range(len(tbl.rows)), key=lambda i: tbl.rows[i][years_idx])
        indices = sorted_indices[:16]
        for i in indices:
            oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle(i)))

    # Strategy 3: Acquire (Intelligent search)
    def strategy_acquire(tbl):
        def wrapper(row):
            idx = tbl.rows.index(row)
            return oracle(idx)
        
        labeled = ezr.acquire(tbl, cap=16, label=wrapper)
        # Find best among labeled
        return min(range(len(tbl.rows)), key=lambda i: ezr.ydist(tbl, oracle(i) if i in labeled_cache else tbl.rows[i]))

    strategies = {
        "random": strategy_random,
        "rule_of_thumb": strategy_rule_of_thumb,
        "acquire": strategy_acquire
    }
    
    results = {}
    for name, func in strategies.items():
        results[name] = func(tbl)
        
    # Determine winner: lowest ydist
    winner = min(results, key=lambda n: ezr.ydist(tbl, oracle(results[n])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for r in rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Oracle
    def label_func(i):
        return rows[i]
    
    result = race(header, masked_rows, label_func)
    
    print("Comparison: Is the 'newest staff' rule of thumb effective?")
    print(f"  Winner: {result['winner']}")
    print(f"  Best Row Index Found: {result['row']}")
    print(f"  Strategies Tried: {', '.join(result['tried'])}")
    
    if result['winner'] == 'rule_of_thumb':
        print("Conclusion: The rule of thumb is effective.")
    else:
        print("Conclusion: The rule of thumb is outperformed by more intelligent search strategies.")
    
    exit(0)
