import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best row within a shared 50-label budget.
    1. random: Picks rows at random.
    2. big_teams: The customer's current strategy (pick rows with high Team Size).
    3. tree_search: Uses the tree-based ranker to guide selection.
    """
    budget = 50
    labeled_indices = set()
    
    def oracle_wrapper(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded!")
            labeled_indices.add(idx)
        return label(idx)

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx, best_ydist = -1, float('inf')
        for i in indices:
            row = oracle_wrapper(i)
            d = ezr.ydist(tbl, row)
            if d < best_ydist:
                best_ydist, best_idx = d, i
        return best_idx, best_ydist

    # Strategy 2: Big Teams (Customer's current way)
    def strategy_big_teams():
        team_idx = header.index("Team Size")
        # Sort by Team Size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
        indices = sorted_indices[:budget // 3]
        best_idx, best_ydist = -1, float('inf')
        for i in indices:
            row = oracle_wrapper(i)
            d = ezr.ydist(tbl, row)
            if d < best_ydist:
                best_ydist, best_idx = d, i
        return best_idx, best_ydist

    # Strategy 3: Tree-based Ranker
    def strategy_tree():
        init_size = 5
        indices = random.sample(range(len(rows)), init_size)
        for i in indices: oracle_wrapper(i)
        
        lab_rows = [label(i) for i in labeled_indices]
        lab_tbl = ezr.Tbl([header] + lab_rows)
        ranker = ezr.ranker(lab_tbl)
        
        unlabeled = [i for i in range(len(rows)) if i not in labeled_indices]
        best_idx = min(unlabeled, key=lambda i: ranker(rows[i]))
        row = oracle_wrapper(best_idx)
        return best_idx, ezr.ydist(tbl, row)

    results = {
        "random": strategy_random(),
        "big_teams": strategy_big_teams(),
        "tree_search": strategy_tree()
    }
    
    winner = min(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    full_rows = [list(r) for r in rows]
    masked_rows = []
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i): return full_rows[i]
    
    random.seed(1234567891)
    result = race(header, masked_rows, label)
    
    print("Analysis: Is 'biggest teams' the best strategy?")
    print(f"Winner: {result['winner']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
    
    if result['winner'] == "big_teams":
        print("Result: Your current strategy of using the biggest teams is optimal.")
    else:
        print(f"Result: No, the '{result['winner']}' strategy outperformed your current approach.")
