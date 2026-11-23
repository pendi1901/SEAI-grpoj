import csv
import random

def race(header, rows, label):
    """
    Compares three strategies to find the best employee record based on goals.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_idx):
        goals = label(row_idx)
        score = 0
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            # '+' columns: maximize, '-' columns: minimize
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategies
    # 1. Random: Pick 16 random rows
    # 2. Tenure-focused: Pick 17 rows with highest 'YearsAtCompany+'
    # 3. Satisfaction-focused: Pick 17 rows with highest 'JobSatisfaction'
    
    strategies = {}
    
    # Strategy: random
    indices = list(range(len(rows)))
    strat_random = random.sample(indices, 16)
    strategies["random"] = strat_random
    
    # Strategy: tenure
    idx_tenure = header.index('YearsAtCompany+')
    strat_tenure = sorted(indices, key=lambda i: rows[i][idx_tenure], reverse=True)[:17]
    strategies["tenure"] = strat_tenure
    
    # Strategy: satisfaction
    idx_sat = header.index('JobSatisfaction')
    strat_sat = sorted(indices, key=lambda i: rows[i][idx_sat], reverse=True)[:17]
    strategies["satisfaction"] = strat_sat
    
    best_overall_score = -float('inf')
    best_overall_row = -1
    winner = ""
    
    for name, sampled_indices in strategies.items():
        for idx in sampled_indices:
            score = get_score(idx)
            if score > best_overall_score:
                best_overall_score = score
                best_overall_row = idx
                winner = name
                
    return {"winner": winner, "row": best_overall_row, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    full_data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            full_data.append(processed)
            
    # Masked rows for the race
    rows = []
    for r in full_data:
        masked = list(r)
        for i, name in enumerate(header):
            if name.endswith('+') or name.endswith('-'):
                masked[i] = "?"
        rows.append(masked)
        
    def label(i):
        goal_indices = [idx for idx, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
        return [full_data[i][idx] for idx in goal_indices]
    
    result = race(header, rows, label)
    
    print("Strategy Race Results:")
    print(f"The winning strategy is: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
