import ezr
import random
import step01
import step07

def race(header, rows, label):
    """
    Compare three strategies: random, acquire (from ezr), and a greedy search.
    Budget: 50 labels total.
    """
    # Shared budget tracker
    labeled_cache = {}
    def oracle_wrapper(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    tbl = ezr.Tbl([header] + rows)
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]

    def get_ydist(idx):
        row = oracle_wrapper(idx)
        return ezr.ydist(tbl, row)

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        return min(indices, key=get_ydist)

    # 2. Acquire Strategy (ezr's built-in)
    def strategy_acquire():
        # Use ezr.acquire to pick rows
        best_idx = step07.choose(header, rows, oracle_wrapper)
        return best_idx

    # 3. Greedy Strategy (Pick rows with lowest xdist to centroid)
    def strategy_greedy():
        centroid = ezr.mids(tbl)
        # Sort by distance to centroid
        candidates = sorted(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[i], centroid))
        # Label top 16
        for i in candidates[:16]:
            oracle_wrapper(i)
        return min(candidates[:16], key=get_ydist)

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "greedy": strategy_greedy()
    }

    # Determine winner (lowest ydist)
    best_name = min(results, key=lambda name: get_ydist(results[name]))
    
    return {
        "winner": best_name,
        "row": results[best_name],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    header = data[0]
    full_rows = [list(r) for r in data[1:]]
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for r in full_rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return full_rows[i]
        
    res = race(header, masked_rows, label)
    
    print(f"Race Results:")
    print(f"Winner: {res['winner']}")
    print(f"Best row index found: {res['row']}")
    print(f"Strategies compared: {', '.join(res['tried'])}")
