import ezr
import random

def race(header, rows, label):
    """
    Compares the customer's rule of thumb against two other strategies.
    Budget: 50 labels total.
    """
    labeled_indices = set()
    
    # We need a table that is updated as we label.
    # Since ezr.Tbl is initialized once, we use a helper to update it.
    tbl = ezr.Tbl([header] + rows)
    
    def oracle_wrapper(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Label budget exceeded!")
            labeled_indices.add(i)
            true_row = label(i)
            # Update the row in the list and the table
            rows[i] = true_row
            ezr.addCols(tbl, true_row)
        return rows[i]

    # Strategy 1: Random
    def strategy_random(rows, oracle):
        indices = random.sample(range(len(rows)), 16)
        for i in indices: oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Rule of Thumb (Biggest pay rises to newest staff)
    def strategy_rule(rows, oracle):
        y_idx = header.index('YearsAtCompany+')
        p_idx = header.index('PercentSalaryHike')
        # Sort by (YearsAtCompany+ asc, PercentSalaryHike desc)
        indices = sorted(range(len(rows)), key=lambda i: (rows[i][y_idx], -rows[i][p_idx]))
        top_indices = indices[:17]
        for i in top_indices: oracle(i)
        return min(top_indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 3: Active Learning
    def strategy_active(rows, oracle):
        # Create a fresh table for the active learner
        local_tbl = ezr.Tbl([header] + rows)
        def local_oracle(row):
            # Find index of this row
            idx = -1
            for i, r in enumerate(rows):
                if r is row: idx = i; break
            return oracle(idx)
        
        ezr.the.Stop = 17
        labeled = ezr.acquire(local_tbl, cap=17, label=local_oracle)
        best_row = min(labeled, key=lambda r: ezr.ydist(local_tbl, r))
        # Find index of best_row
        for i, r in enumerate(rows):
            if r is best_row: return i
        return 0

    results = {
        "random": strategy_random(rows, oracle_wrapper),
        "rule_of_thumb": strategy_rule(rows, oracle_wrapper),
        "active": strategy_active(rows, oracle_wrapper)
    }
    
    # Find winner (lowest ydist)
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "rule_of_thumb", "active"]
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    full_data = [list(r) for r in rows]
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    masked_rows = []
    for r in rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
            
    def label(i): return full_data[i]
    
    result = race(header, masked_rows, label)
    
    print("Analysis: Comparing the 'Rule of Thumb' (pay rises to new staff) vs other strategies.")
    print(f"Winner: {result['winner']}")
    print(f"The 'rule_of_thumb' strategy was {'better' if result['winner'] == 'rule_of_thumb' else 'worse'} than the alternatives.")
    print("The active learning strategy typically outperforms simple heuristics by exploring the data space intelligently.")
    
    exit(0)
