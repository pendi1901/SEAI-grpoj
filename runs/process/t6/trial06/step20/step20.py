import ezr
import step01
import step02
import step07
import step10
import random

def race(header, rows, label):
    """
    Compares strategies: 'random', 'big_teams' (customer's current approach), 
    and 'tree_search' (our approach). Total budget: 50 labels.
    """
    budget = 50
    labeled_indices = {}

    def get_label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # 1. Random strategy
    def run_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices:
            goals = get_label(i)
            for j, val in enumerate(goals):
                rows[i][9 + j] = val
        return min([i for i in indices if "?" not in rows[i][9:]], 
                   key=lambda i: ezr.ydist(ezr.Tbl([header] + rows), rows[i]), default=-1)

    # 2. Big Teams strategy (Customer's current approach)
    def run_big_teams():
        # Sort by Team Size (index 8) descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][8], reverse=True)
        indices = sorted_indices[:budget // 3]
        for i in indices:
            goals = get_label(i)
            for j, val in enumerate(goals):
                rows[i][9 + j] = val
        return min([i for i in indices if "?" not in rows[i][9:]], 
                   key=lambda i: ezr.ydist(ezr.Tbl([header] + rows), rows[i]), default=-1)

    # 3. Tree Search strategy (Our approach)
    def run_tree():
        tbl = ezr.Tbl([header] + rows)
        def oracle_wrapper(r):
            idx = rows.index(r)
            goals = get_label(idx)
            for j, val in enumerate(goals):
                r[9 + j] = val
            return r
        labeled = ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)
        best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Execute
    res_random = run_random()
    res_big = run_big_teams()
    res_tree = run_tree()

    # Evaluate results
    tbl = ezr.Tbl([header] + rows)
    def get_ydist(i):
        return ezr.ydist(tbl, rows[i]) if i != -1 else 1e30

    results = {
        "random": res_random,
        "big_teams": res_big,
        "tree_search": res_tree
    }
    
    winner = min(results, key=lambda k: get_ydist(results[k]))
    return {"winner": winner, "row": results[winner], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    for r in rows:
        r[9] = r[10] = r[11] = "?"
        
    full_data = list(ezr.csv(filename))
    full_rows = full_data[1:]
    
    def label_func(i):
        return [full_rows[i][9], full_rows[i][10], full_rows[i][11]]
    
    res = race(header, rows, label_func)
    print(f"Comparison Results: The '{res['winner']}' strategy found the best configuration.")
    print(f"The best row found was at index {res['row']}.")
    print(f"Strategies compared: {', '.join(res['tried'])}")
    
    if res['winner'] == 'tree_search':
        print("\nConclusion: Our tree-based approach outperforms the 'big teams' strategy.")
    else:
        print("\nConclusion: The 'big teams' strategy remains competitive.")
    exit(0)
