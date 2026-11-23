import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee row:
    1. 'random': Picks 17 rows at random.
    2. 'tenure_focus': Picks 17 rows with high 'TotalWorkingYears'.
    3. 'satisfaction_focus': Picks 16 rows with high 'JobSatisfaction'.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategies definitions
    strategies = {
        "random": 17,
        "tenure_focus": 17,
        "satisfaction_focus": 16
    }
    
    results = {}
    labeled_count = 0
    
    for name, count in strategies.items():
        best_idx = -1
        best_score = float('-inf')
        
        candidates = []
        if name == "random":
            candidates = random.sample(range(len(rows)), count)
        elif name == "tenure_focus":
            # Sort by TotalWorkingYears (index 28)
            idx_twy = header.index('TotalWorkingYears')
            sorted_rows = sorted(range(len(rows)), key=lambda i: rows[i][idx_twy], reverse=True)
            candidates = sorted_rows[:count]
        elif name == "satisfaction_focus":
            # Sort by JobSatisfaction (index 16)
            idx_js = header.index('JobSatisfaction')
            sorted_rows = sorted(range(len(rows)), key=lambda i: rows[i][idx_js], reverse=True)
            candidates = sorted_rows[:count]
            
        for idx in candidates:
            true_goals = label(idx)
            score = get_score(true_goals)
            if score > best_score:
                best_score = score
                best_idx = idx
            labeled_count += 1
            
        results[name] = (best_score, best_idx)

    # Determine winner
    winner = max(results, key=lambda k: results[k][0])
    
    return {
        "winner": winner,
        "row": results[winner][1],
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

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    true_data = {i: [rows[i][g] for g in goal_indices] for i in range(len(rows))}
    
    # Mask rows
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    def label(i):
        return true_data[i]

    outcome = race(header, rows, label)
    
    print("Strategy Race Results:")
    print(f"The winning strategy is: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
