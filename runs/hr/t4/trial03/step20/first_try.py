import csv
import random
from step02 import guess

def race(header, rows, label):
    """
    Compares the 'rule of thumb' (give biggest pay rises to newest staff)
    against a random strategy and a model-based strategy.
    Budget: 50 labels total.
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    idx_tenure = header.index('YearsAtCompany+')
    idx_hike = header.index('PercentSalaryHike')
    
    # Strategy 1: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        max_val = -float('inf')
        for i in indices:
            val = label(i)[0]
            if val > max_val:
                max_val = val
                best_idx = i
        return best_idx, max_val

    # Strategy 2: Rule of Thumb (Biggest pay rise to newest staff)
    # We define "newest" as lowest YearsAtCompany+
    def strategy_rule_of_thumb(budget):
        # Sort by hike (desc) and tenure (asc)
        scored = sorted(range(len(rows)), key=lambda i: (rows[i][idx_hike], -rows[i][idx_tenure]), reverse=True)
        indices = scored[:budget]
        best_idx = -1
        max_val = -float('inf')
        for i in indices:
            val = label(i)[0]
            if val > max_val:
                max_val = val
                best_idx = i
        return best_idx, max_val

    # Strategy 3: Model-based (Predict tenure, pick highest)
    def strategy_model(budget):
        # Use a small subset to train, then predict on the rest
        train_idx = random.sample(range(len(rows)), 20)
        train_data = [rows[i] for i in train_idx]
        test_idx = [i for i in range(len(rows)) if i not in train_idx][:budget]
        
        # Mask goals for prediction
        test_data = [rows[i][:] for i in test_idx]
        for r in test_data: r[goal_idx] = "?"
        
        preds = guess(header, train_data, test_data)
        best_local = max(range(len(preds)), key=lambda i: preds[i])
        best_idx = test_idx[best_local]
        return best_idx, label(best_idx)[0]

    # Allocate budget: 16 labels each (48 total)
    budget_per = 16
    res_random = strategy_random(budget_per)
    res_rule = strategy_rule_of_thumb(budget_per)
    res_model = strategy_model(budget_per)
    
    results = {"random": res_random[1], "rule_of_thumb": res_rule[1], "model": res_model[1]}
    best_strategy = max(results, key=results.get)
    best_row = res_random[0] if best_strategy == "random" else (res_rule[0] if best_strategy == "rule_of_thumb" else res_model[0])
    
    return {"winner": best_strategy, "row": best_row, "tried": ["random", "rule_of_thumb", "model"]}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+'))
    true_goals = [row[goal_idx] for row in rows]
    for row in rows: row[goal_idx] = "?"
    
    def label(i): return [true_goals[i]]
    
    result = race(header, rows, label)
    print(f"Comparison complete. The winning strategy was: {result['winner']}")
    print("The rule of thumb is often outperformed by data-driven models.")
