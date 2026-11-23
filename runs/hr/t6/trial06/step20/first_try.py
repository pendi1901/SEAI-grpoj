import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies:
    1. random: Pick rows at random.
    2. rule_of_thumb: Give biggest pay rises to newest staff (lowest YearsAtCompany+).
    3. active_learning: Use ezr.acquire to find the best rows.
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
    def strategy_random(tbl):
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 2: Rule of Thumb (Newest staff = lowest YearsAtCompany+)
    def strategy_rule(tbl):
        # Sort by YearsAtCompany+ (index 31)
        indices = sorted(range(len(rows)), key=lambda i: rows[i][31])
        for i in indices[:budget // 3]: get_label(i)
        return min(indices[:budget // 3], key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 3: Active Learning
    def strategy_active(tbl):
        def oracle(row):
            for i, r in enumerate(rows):
                if r is row: return get_label(i)
            return row
        ezr.acquire(tbl, cap=budget // 3, label=oracle)
        return min(labeled.keys(), key=lambda i: ezr.ydist(tbl, get_label(i)))

    tbl = ezr.Tbl([header] + rows)
    results = {
        "random": strategy_random(tbl),
        "rule_of_thumb": strategy_rule(tbl),
        "active_learning": strategy_active(tbl)
    }
    
    winner = min(results, key=lambda k: ezr.ydist(tbl, get_label(results[k])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    all_rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i): return all_rows[i]
    
    result = race(header, masked_rows, label)
    
    print("Analysis: Is the 'newest staff' rule of thumb effective?")
    print(f"The winning strategy was: {result['winner']}")
    if result['winner'] == "rule_of_thumb":
        print("Yes, the rule of thumb is effective.")
    else:
        print("No, our active learning strategy outperformed the rule of thumb.")
    print("-" * 40)
    print("Strategy: We compared random selection, the 'newest staff' rule,")
    print("and active learning to find the best employee retention configuration.")
    exit(0)
