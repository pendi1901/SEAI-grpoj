import ezr
import random
import step10

def race(header, rows, label):
    """
    Compare the 'rule of thumb' (pay rises to newest staff) against 
    random and tree-based strategies.
    """
    budget = 50
    labeled_cache = {}

    def get_label(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
            for j, col_idx in enumerate(goal_indices):
                rows[i][col_idx] = labeled_cache[i][j]
        return labeled_cache[i]

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    tbl = ezr.Tbl([header] + rows)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Rule of Thumb (Biggest pay rise to newest staff)
    # "Newest" = lowest YearsAtCompany. "Biggest pay rise" = highest PercentSalaryHike.
    # We prioritize those with low tenure and high salary hike potential.
    def strategy_rule_of_thumb():
        tenure_idx = header.index('YearsAtCompany+')
        hike_idx = header.index('PercentSalaryHike')
        # Sort by lowest tenure, then highest hike
        candidates = sorted(range(len(rows)), key=lambda i: (rows[i][tenure_idx], -rows[i][hike_idx]))
        indices = candidates[:budget // 3]
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 3: Tree-based
    def strategy_tree():
        indices = random.sample(range(len(rows)), 10)
        for i in indices: get_label(i)
        lab_rows = [rows[i] for i in labeled_cache.keys()]
        lab_tbl = ezr.clone(tbl, lab_rows)
        ranker = ezr.ranker(lab_tbl)
        candidates = [i for i in range(len(rows)) if i not in labeled_cache]
        best_i = min(candidates, key=lambda i: ranker(rows[i]))
        get_label(best_i)
        return best_i

    results = {
        "random": strategy_random(),
        "rule_of_thumb": strategy_rule_of_thumb(),
        "tree": strategy_tree()
    }
    
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    return {"winner": winner, "row": results[winner], "tried": list(results.keys())}

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    original_rows = [list(r) for r in rows]
    
    def label(i):
        return [original_rows[i][idx] for idx in goal_indices]
    
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    result = race(header, rows, label)
    print(f"Analysis: Is the 'rule of thumb' (pay rises to new staff) effective?")
    print(f"The winning strategy was: {result['winner']}.")
    print(f"The best arrangement found was at index {result['row']}.")
    if result['winner'] == "rule_of_thumb":
        print("Conclusion: Your rule of thumb is highly effective.")
    else:
        print("Conclusion: Our data-driven strategies outperformed your rule of thumb.")
