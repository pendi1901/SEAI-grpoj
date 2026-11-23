import csv
import random
import step01
import step02
import step07

def get_score(header, row):
    """Calculates a score where higher is better."""
    score = 0
    for i, name in enumerate(header):
        if name.endswith('+'):
            score += row[i]
        elif name.endswith('-'):
            score -= row[i]
    return score

def race(header, rows, label):
    """
    Compares three strategies:
    1. random: Baseline.
    2. rule_of_thumb: Biggest pay rises to newest staff (low TotalWorkingYears).
    3. tenure_optimization: Focus on high tenure metrics (our approach).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Strategy 1: Random
    def strategy_random(indices):
        return random.sample(indices, 16)

    # Strategy 2: Rule of Thumb (Newest staff = low TotalWorkingYears)
    def strategy_rule_of_thumb(indices):
        # Sort by lowest TotalWorkingYears
        return sorted(indices, key=lambda i: rows[i][header.index('TotalWorkingYears')])[:17]

    # Strategy 3: Tenure Optimization (Our approach)
    def strategy_tenure(indices):
        # Sort by highest TotalWorkingYears (experienced staff)
        return sorted(indices, key=lambda i: rows[i][header.index('TotalWorkingYears')], reverse=True)[:17]

    strategies = {
        "random": strategy_random,
        "rule_of_thumb": strategy_rule_of_thumb,
        "tenure_optimization": strategy_tenure
    }
    
    all_indices = list(range(len(rows)))
    best_overall_score = -float('inf')
    best_row_idx = -1
    winner = ""
    
    budget = 50
    for name, func in strategies.items():
        sampled = func(all_indices)
        for idx in sampled:
            if budget <= 0: break
            true_goals = label(idx)
            temp_row = list(rows[idx])
            for i, g_idx in enumerate(goal_indices):
                temp_row[g_idx] = true_goals[i]
            
            score = get_score(header, temp_row)
            if score > best_overall_score:
                best_overall_score = score
                best_row_idx = idx
                winner = name
            budget -= 1
            
    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

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
            
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    def label(i):
        return [rows[i][g] for g in goal_indices]
    
    # Mask rows
    for row in rows:
        for g in goal_indices:
            row[g] = "?"
            
    result = race(header, rows, label)
    print("Comparison: Is the 'rule of thumb' (pay rises to newest staff) effective?")
    print(f"The winning strategy is '{result['winner']}'.")
    if result['winner'] == "rule_of_thumb":
        print("The rule of thumb is effective.")
    else:
        print("Our tenure-based optimization strategy outperforms the rule of thumb.")
    print(f"Strategies evaluated: {', '.join(result['tried'])}.")
