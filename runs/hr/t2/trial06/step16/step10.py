import csv
import random
import step01
import step07

def race(header, rows, label):
    """
    Compares three strategies for finding the best row:
    1. random: Samples rows randomly.
    2. top_tenure: Samples rows with the highest tenure (YearsAtCompany+).
    3. top_manager: Samples rows with the highest years with current manager.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_idx):
        true_goals = label(row_idx)
        score = 0
        for i, goal_idx in enumerate(goal_indices):
            val = true_goals[i]
            if header[goal_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategies
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        return {idx: get_score(idx) for idx in indices}

    def strategy_top_tenure(budget):
        # Use YearsAtCompany+ (index 31)
        idx_tenure = header.index('YearsAtCompany+')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][idx_tenure], reverse=True)
        indices = sorted_indices[:budget]
        return {idx: get_score(idx) for idx in indices}

    def strategy_top_manager(budget):
        # Use YearsWithCurrManager+ (index 34)
        idx_mgr = header.index('YearsWithCurrManager+')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][idx_mgr], reverse=True)
        indices = sorted_indices[:budget]
        return {idx: get_score(idx) for idx in indices}

    # Budget is 50, split between 3 strategies
    budget_per = 16
    results = {
        "random": strategy_random(budget_per),
        "top_tenure": strategy_top_tenure(budget_per),
        "top_manager": strategy_top_manager(budget_per)
    }

    best_overall_score = float('-inf')
    winner = None
    best_row = -1

    for name, data in results.items():
        for idx, score in data.items():
            if score > best_overall_score:
                best_overall_score = score
                winner = name
                best_row = idx

    return {"winner": winner, "row": best_row, "tried": list(results.keys())}

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Mask rows
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    def label(i):
        # Re-read original file to get true values for the harness
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for count, row in enumerate(reader):
                if count == i:
                    return [float(row[idx]) if header[idx][0].isupper() else row[idx] for idx in goal_indices]
        return []

    result = race(header, rows, label)
    print(f"Strategy Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best Row Found: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
