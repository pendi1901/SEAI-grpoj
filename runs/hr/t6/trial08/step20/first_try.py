import ezr
import random
import step01
import step10

def race(header, rows, label):
    """
    Compare the customer's rule of thumb against our AI strategies.
    Budget: 50 labels total.
    """
    budget = 50
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    def get_ydist(row):
        tbl = ezr.Tbl([header, row])
        return ezr.ydist(tbl, row)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx = -1
        best_ydist = 1e30
        for idx in indices:
            full_row = oracle_wrapper(idx)
            d = get_ydist(full_row)
            if d < best_ydist:
                best_ydist, best_idx = d, idx
        return best_idx, best_ydist

    # Strategy 2: Rule of Thumb (Biggest pay rises to newest staff)
    # Newest staff = low YearsAtCompany (index 31).
    # We define "biggest pay rise" as high PercentSalaryHike (index 17).
    # We prioritize rows with low YearsAtCompany and high PercentSalaryHike.
    def strategy_rule_of_thumb():
        # Sort by tenure (asc) then hike (desc)
        indices = sorted(range(len(rows)), key=lambda i: (rows[i][31], -rows[i][17]))
        best_idx = -1
        best_ydist = 1e30
        for idx in indices[:budget // 3]:
            full_row = oracle_wrapper(idx)
            d = get_ydist(full_row)
            if d < best_ydist:
                best_ydist, best_idx = d, idx
        return best_idx, best_ydist

    # Strategy 3: AI-Driven (Greedy search)
    def strategy_ai():
        indexed_rows = [list(r) + [i] for i, r in enumerate(rows)]
        tbl = ezr.Tbl([header + ["idxX"]] + indexed_rows)
        def oracle_proxy(row):
            idx = int(row[-1])
            full = oracle_wrapper(idx)
            for i in range(len(header)): row[i] = full[i]
            return row
        labeled = ezr.acquire(tbl, cap=budget // 3, label=oracle_proxy)
        best = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        return int(best[-1]), ezr.ydist(tbl, best)

    results = {
        "random": strategy_random(),
        "rule_of_thumb": strategy_rule_of_thumb(),
        "ai_driven": strategy_ai()
    }

    winner = min(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    def real_label(i):
        return rows[i]

    outcome = race(header, rows, real_label)
    print("Strategy Comparison: Rule of Thumb vs AI")
    print("-" * 50)
    print(f"Winner: {outcome['winner']}")
    print(f"Best Row Index Found: {outcome['row']}")
    print(f"Strategies Tried: {', '.join(outcome['tried'])}")
    print("-" * 50)
    if outcome['winner'] == "rule_of_thumb":
        print("The rule of thumb is effective for this dataset.")
    else:
        print("The AI-driven strategy outperformed the rule of thumb.")
