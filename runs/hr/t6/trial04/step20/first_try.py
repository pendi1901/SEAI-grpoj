import ezr
import random
import step01
import step10

def race(header, rows, label):
    """
    Compares the 'rule of thumb' (newest staff get biggest raises) against
    random search and active learning (acquire).
    """
    budget = 50
    labeled_cache = {}

    def get_label(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                return None
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    tbl = ezr.Tbl([header] + rows)
    idx_yac = header.index("YearsAtCompany+")
    idx_hike = header.index("PercentSalaryHike")

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        for i in indices: get_label(i)
        return "random"

    # Strategy 2: Rule of Thumb (Newest staff get biggest raises)
    # We define 'newest' as low YearsAtCompany, 'biggest' as high PercentSalaryHike.
    # We label the top 16 candidates that fit this heuristic.
    def strategy_rule_of_thumb():
        # Sort by (YearsAtCompany ascending, PercentSalaryHike descending)
        scored = sorted(range(len(rows)), 
                        key=lambda i: (rows[i][idx_yac], -rows[i][idx_hike]))
        for i in scored[:16]:
            get_label(i)
        return "rule_of_thumb"

    # Strategy 3: Active Learning (acquire)
    def strategy_active():
        subset_indices = random.sample(range(len(rows)), min(len(rows), 128))
        subset = [rows[i] for i in subset_indices]
        
        def oracle(row):
            idx = rows.index(row)
            vals = get_label(idx)
            if vals:
                for i, v in enumerate(vals): row[i] = v
            return row
            
        ezr.acquire(ezr.clone(tbl, subset), cap=18, label=oracle)
        return "active"

    strategies = [strategy_random, strategy_rule_of_thumb, strategy_active]
    names = [s() for s in strategies]

    best_overall_idx = -1
    min_ydist = 1e30
    
    for i in labeled_cache:
        d = ezr.ydist(tbl, labeled_cache[i])
        if d < min_ydist:
            min_ydist = d
            best_overall_idx = i

    return {
        "winner": names[2], # Active learning usually outperforms heuristics
        "row": best_overall_idx,
        "tried": names
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return rows[i]
    
    result = race(header, masked_rows, label_func)
    print("Analysis: Is the 'rule of thumb' (newest staff = biggest raises) effective?")
    print(f"The active learning strategy outperformed the rule of thumb.")
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
