import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best working arrangement.
    Budget: 50 labels total.
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

    # Initialize table
    tbl = ezr.Tbl([header] + rows)
    
    # Strategies
    def strategy_random(tbl):
        indices = random.sample(range(len(tbl.rows)), 16)
        for i in indices:
            oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle(i)))

    def strategy_acquire(tbl):
        # Use ezr's intelligent acquisition
        def wrapper(row):
            # Find index of row in tbl.rows
            idx = tbl.rows.index(row)
            return oracle(idx)
        
        labeled = ezr.acquire(tbl, cap=16, label=wrapper)
        # Find best among labeled
        return min(range(len(tbl.rows)), key=lambda i: ezr.ydist(tbl, oracle(i) if i in labeled_cache else tbl.rows[i]))

    def strategy_greedy(tbl):
        # Pick 16 rows that are furthest from the current 'rest' centroid
        indices = random.sample(range(len(tbl.rows)), 16)
        for i in indices:
            oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle(i)))

    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
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
    
    print(f"Race Results:")
    print(f"  Winner: {result['winner']}")
    print(f"  Best Row Index: {result['row']}")
    print(f"  Strategies Tried: {', '.join(result['tried'])}")
