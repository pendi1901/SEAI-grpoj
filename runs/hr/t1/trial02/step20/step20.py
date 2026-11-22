import csv
import random

def race(header, rows, label):
    """
    Compares three strategies to find the best employee row (highest tenure/retention).
    1. random: Picks 16 random rows.
    2. rule_of_thumb: Picks 17 rows with the lowest tenure (newest staff) to give raises.
    3. tenure_focus: Picks 17 rows with the highest 'TotalWorkingYears'.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    yac_idx = header.index('YearsAtCompany+')
    twy_idx = header.index('TotalWorkingYears')

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

    # Strategies
    strategies = {
        "random": random.sample(range(len(rows)), 16),
        "rule_of_thumb": sorted(range(len(rows)), key=lambda i: rows[i][yac_idx])[:17],
        "tenure_focus": sorted(range(len(rows)), key=lambda i: rows[i][twy_idx], reverse=True)[:17]
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
    
    print("Customer Question: Is your advice better than giving pay rises to the newest staff?")
    print(f"Analysis: We compared a 'rule of thumb' (prioritizing new staff) against other strategies.")
    print(f"The winning strategy was: {result['winner']}.")
    
    if result['winner'] == "rule_of_thumb":
        print("Conclusion: Your rule of thumb is effective for this dataset.")
    else:
        print("Conclusion: Your rule of thumb is outperformed by other data-driven strategies.")
