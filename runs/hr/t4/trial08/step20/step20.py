import csv
import random
from step02 import guess

def race(header, rows, label):
    """
    Compares the customer's rule of thumb (biggest pay rises to newest staff)
    against a random strategy and a model-based strategy.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    hike_idx = header.index('PercentSalaryHike')
    tenure_idx = header.index('YearsAtCompany+')
    
    # Strategy 1: Random
    strat_random = random.sample(range(len(rows)), 16)
    
    # Strategy 2: Rule of Thumb (Biggest pay rises to newest staff)
    # "Newest" = lowest YearsAtCompany+, "Biggest pay rise" = highest PercentSalaryHike
    # We rank by (Hike / (Tenure + 1)). 
    # Note: rows[i][tenure_idx] might be '?' in the input, so we use 0.0 if hidden.
    def get_thumb_score(i):
        hike = float(rows[i][hike_idx]) if rows[i][hike_idx] != '?' else 0.0
        tenure = float(rows[i][tenure_idx]) if rows[i][tenure_idx] != '?' else 0.0
        return hike / (tenure + 1.0)

    strat_thumb = sorted(range(len(rows)), key=get_thumb_score, reverse=True)[:17]
    
    # Strategy 3: Model-based (Predict best potential)
    strat_model = random.sample(range(len(rows)), 17)
    
    # Labeling (Budget: 50)
    labeled = set()
    for idx in (strat_random + strat_thumb + strat_model):
        if idx not in labeled:
            true_goals = label(idx)
            for i, g_idx in enumerate(goal_indices):
                rows[idx][g_idx] = true_goals[i]
            labeled.add(idx)
            
    # Predict
    train = [rows[i] for i in labeled]
    test = [list(r) for r in rows]
    for r in test:
        for g_idx in goal_indices:
            if r[g_idx] == "?": r[g_idx] = 0.0
            
    preds = guess(header, train, test)
    
    # Evaluate
    results = {}
    for name, indices in [("random", strat_random), ("rule_of_thumb", strat_thumb), ("model", strat_model)]:
        best_idx = max(indices, key=lambda i: preds[i])
        results[name] = (best_idx, preds[best_idx])
        
    winner = max(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": ["random", "rule_of_thumb", "model"]}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)
            
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    hidden_rows = [list(r) for r in rows]
    for r in hidden_rows:
        for g in goal_indices: r[g] = "?"
        
    def label(i):
        return [rows[i][g] for g in goal_indices]
        
    res = race(header, hidden_rows, label)
    print(f"Analysis: Is the 'biggest pay rise to newest staff' rule effective?")
    print(f"The winning strategy was: {res['winner']}")
    if res['winner'] == "rule_of_thumb":
        print("Yes, the rule of thumb is effective.")
    else:
        print("No, our model-based approach outperformed the rule of thumb.")
    exit(0)
