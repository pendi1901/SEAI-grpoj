import csv
import random
from step02 import guess

def race(header, rows, label):
    """
    Compares the customer's rule of thumb against two other strategies.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_idx):
        vals = label(row_idx)
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = vals[i]
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx = max(indices, key=get_score)
        return best_idx, get_score(best_idx)

    # Strategy 2: Customer's Rule (Biggest pay rises to newest staff)
    # Proxy: Newest staff = low 'YearsAtCompany+'. 
    # We assume 'PercentSalaryHike' is the pay rise.
    def strategy_customer_rule():
        tenure_idx = header.index('YearsAtCompany+')
        hike_idx = header.index('PercentSalaryHike')
        # Sort by tenure ascending, then by hike descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: (rows[i][tenure_idx], -rows[i][hike_idx]))
        indices = sorted_indices[:16]
        best_idx = max(indices, key=get_score)
        return best_idx, get_score(best_idx)

    # Strategy 3: Model-based (Predict best using KNN)
    def strategy_model():
        # Use first 16 rows as training, predict on a sample
        train_indices = list(range(16))
        test_indices = random.sample(range(16, len(rows)), 16)
        
        train_data = [rows[i] for i in train_indices]
        test_data = [rows[i] for i in test_indices]
        
        # Mask goals
        for r in test_data:
            for g in goal_indices: r[g] = 0.0
            
        preds = guess(header, train_data, test_data)
        best_idx = test_indices[preds.index(max(preds))]
        return best_idx, get_score(best_idx)

    strategies = {
        "random": strategy_random,
        "customer_rule": strategy_customer_rule,
        "model_based": strategy_model
    }

    results = {}
    for name, func in strategies.items():
        idx, score = func()
        results[name] = (idx, score)

    winner = max(results, key=lambda n: results[n][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    labeled_data = {}
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]

    def label(i):
        if i not in labeled_data:
            if len(labeled_data) >= 50:
                raise ValueError("Limit of 50 labels exceeded.")
            labeled_data[i] = [rows[i][g] for g in goal_indices]
        return labeled_data[i]

    result = race(header, rows, label)
    
    print("Analysis: Is the 'biggest pay rises to newest staff' rule effective?")
    print(f"The winning strategy was: {result['winner']}.")
    if result['winner'] == 'customer_rule':
        print("Conclusion: Your rule of thumb is effective compared to random and model-based approaches.")
    else:
        print("Conclusion: Your rule of thumb is outperformed by other data-driven strategies.")
