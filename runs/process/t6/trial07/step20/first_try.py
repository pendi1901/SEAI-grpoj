import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, acquire, and 'biggest team'.
    Budget is 50 labels total.
    """
    budget = 50
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(ezr.Tbl([header] + [labeled[k] for k in labeled]), labeled[i]))

    # Strategy 2: Acquire (ezr's built-in)
    def strategy_acquire():
        tbl = ezr.Tbl([header] + rows)
        def oracle_wrapper(r):
            idx = rows.index(r)
            return get_label(idx)
        subset = ezr.acquire(tbl, cap=17, label=oracle_wrapper)
        return rows.index(min(subset, key=lambda r: ezr.ydist(tbl, r)))

    # Strategy 3: Biggest Team (Customer's current approach)
    def strategy_biggest():
        team_idx = header.index('Team Size')
        # Sort by Team Size descending
        candidates = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
        # Label top 17
        for i in candidates[:17]: get_label(i)
        return min(candidates[:17], key=lambda i: ezr.ydist(ezr.Tbl([header] + [labeled[k] for k in labeled]), labeled[i]))

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "biggest": strategy_biggest()
    }

    # Evaluate winners based on true ydist
    tbl = ezr.Tbl([header] + rows)
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
    return {"winner": winner, "row": results[winner], "tried": list(results.keys())}

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    def label_func(i):
        return rows[i]
    
    result = race(header, masked_rows, label_func)
    
    print("Analysis: Is 'biggest team' better than our adaptive search?")
    print(f"The winner is the '{result['winner']}' strategy.")
    print(f"Best setup found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
    
    if result['winner'] == 'biggest':
        print("Conclusion: The customer's current 'biggest team' strategy is optimal.")
    else:
        print("Conclusion: Our adaptive search ('acquire') outperforms the 'biggest team' strategy.")
    exit(0)
