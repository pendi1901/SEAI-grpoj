import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee (highest YearsAtCompany+).
    Budget: 50 labels total.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Track labels used to respect the 50-label budget
    labeled_cache = {}
    def get_label(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_i = indices[0]
        best_val = get_label(best_i)[0]
        for i in indices[1:]:
            val = get_label(i)[0]
            if val > best_val:
                best_val, best_i = val, i
        return best_i, best_val

    def strategy_top_tenure():
        # Heuristic: Sample rows with high 'TotalWorkingYears' as a proxy for 'YearsAtCompany+'
        twy_idx = header.index('TotalWorkingYears')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][twy_idx], reverse=True)
        best_i = sorted_indices[0]
        best_val = get_label(best_i)[0]
        for i in sorted_indices[1:17]:
            val = get_label(i)[0]
            if val > best_val:
                best_val, best_i = val, i
        return best_i, best_val

    def strategy_high_income():
        # Heuristic: Sample rows with high 'MonthlyIncome'
        inc_idx = header.index('MonthlyIncome')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][inc_idx], reverse=True)
        best_i = sorted_indices[0]
        best_val = get_label(best_i)[0]
        for i in sorted_indices[1:17]:
            val = get_label(i)[0]
            if val > best_val:
                best_val, best_i = val, i
        return best_i, best_val

    strategies = {
        "random": strategy_random,
        "tenure_proxy": strategy_top_tenure,
        "income_proxy": strategy_high_income
    }

    results = {}
    best_overall_val = -float('inf')
    winner = None
    best_row_idx = -1

    for name, func in strategies.items():
        idx, val = func()
        results[name] = val
        if val > best_overall_val:
            best_overall_val = val
            winner = name
            best_row_idx = idx

    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    def label(i):
        return [rows[i][goal_idx]]

    outcome = race(header, rows, label)
    
    print("Strategy Race Results:")
    print(f"Winner: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
