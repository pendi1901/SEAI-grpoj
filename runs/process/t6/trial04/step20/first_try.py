import ezr
import step10
import random

def race(header, rows, label):
    """
    Compare 'random' search, 'acquire' (ezr's smart search), and 'big_teams'
    (the customer's current strategy of picking rows with large team sizes).
    """
    budget = 50
    labeled_indices = {}

    def oracle_wrapper(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                return None
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    tbl = ezr.Tbl([header] + rows)
    team_idx = header.index("Team Size")

    def strategy_random(budget_per):
        indices = random.sample(range(len(rows)), budget_per)
        return [oracle_wrapper(i) for i in indices if oracle_wrapper(i) is not None]

    def strategy_acquire(budget_per):
        ezr.the.Stop = budget_per
        def local_label(r):
            for i, row in enumerate(rows):
                if row is r: return oracle_wrapper(i)
            return r
        return ezr.acquire(tbl, cap=budget_per, label=local_label)

    def strategy_big_teams(budget_per):
        # Customer strategy: pick rows with the largest team sizes
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
        return [oracle_wrapper(i) for i in sorted_indices[:budget_per] if oracle_wrapper(i) is not None]

    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "big_teams": strategy_big_teams
    }
    
    budget_per = budget // len(strategies)
    best_overall_ydist = float('inf')
    winner = None
    best_row_idx = -1

    for name, func in strategies.items():
        labeled = func(budget_per)
        for r in labeled:
            d = ezr.ydist(tbl, r)
            if d < best_overall_ydist:
                best_overall_ydist = d
                winner = name
                for i, row in enumerate(rows):
                    if row is r:
                        best_row_idx = i
                        break

    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    def label(i):
        return rows[i]
    
    result = race(header, masked_rows, label)
    
    print("Optimization Strategy Comparison:")
    print("-" * 40)
    print(f"Winner: {result['winner']}")
    print(f"Best Row Index: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
    print("-" * 40)
    print("Conclusion: If 'acquire' wins, your current 'big_teams' strategy")
    print("is likely suboptimal compared to data-driven search.")
