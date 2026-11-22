import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee row within a 50-label budget.
    Strategies:
    1. random: Picks 16 random rows.
    2. tenure_focus: Picks 17 rows with the highest 'TotalWorkingYears'.
    3. satisfaction_focus: Picks 17 rows with the highest 'JobSatisfaction'.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_idx):
        goals = label(row_idx)
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategy definitions
    strategies = {
        "random": random.sample(range(len(rows)), 16),
        "tenure_focus": sorted(range(len(rows)), key=lambda i: rows[i][header.index('TotalWorkingYears')], reverse=True)[:17],
        "satisfaction_focus": sorted(range(len(rows)), key=lambda i: rows[i][header.index('JobSatisfaction')], reverse=True)[:17]
    }

    best_overall_score = -float('inf')
    best_overall_row = -1
    winner = ""

    for name, indices in strategies.items():
        best_strat_score = -float('inf')
        best_strat_row = -1
        for idx in indices:
            score = get_score(idx)
            if score > best_strat_score:
                best_strat_score = score
                best_strat_row = idx
        
        if best_strat_score > best_overall_score:
            best_overall_score = best_strat_score
            best_overall_row = best_strat_row
            winner = name

    return {"winner": winner, "row": best_overall_row, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)

    labeled = set()
    def label(i):
        if len(labeled) >= 50 and i not in labeled:
            raise Exception("Exceeded 50 labels")
        labeled.add(i)
        return [rows[i][idx] for idx in goal_indices]

    result = race(header, masked_rows, label)
    
    print(f"Race complete. Strategies tried: {', '.join(result['tried'])}")
    print(f"The winning strategy was: {result['winner']}")
    print(f"The best row found was index {result['row']}.")
