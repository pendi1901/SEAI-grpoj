import csv
import random

def race(header, rows, label):
    """
    Compares three strategies to find the best row using a shared budget of 50 labels.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_idx):
        """Returns a normalized score where higher is better."""
        goals = label(row_idx)
        score = 0.0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            # For simplicity, we assume goal columns are numeric.
            # Normalize: if +, higher is better; if -, lower is better.
            # This is a heuristic to compare rows.
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategies
    def random_strategy(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        best_val = -float('inf')
        for idx in indices:
            val = get_score(idx)
            if val > best_val:
                best_val = val
                best_idx = idx
        return best_idx

    def greedy_strategy(budget):
        # Sample a few, then pick the best
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        best_val = -float('inf')
        for idx in indices:
            val = get_score(idx)
            if val > best_val:
                best_val = val
                best_idx = idx
        return best_idx

    def extreme_strategy(budget):
        # Focus on rows with high 'TotalWorkingYears' as a proxy for 'best'
        years_idx = header.index('TotalWorkingYears')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][years_idx], reverse=True)
        best_idx = -1
        best_val = -float('inf')
        for idx in sorted_indices[:budget]:
            val = get_score(idx)
            if val > best_val:
                best_val = val
                best_idx = idx
        return best_idx

    # Budget allocation: 16 + 17 + 17 = 50
    strategies = {
        "random": (random_strategy, 16),
        "greedy": (greedy_strategy, 17),
        "extreme": (extreme_strategy, 17)
    }
    
    results = {}
    best_overall_idx = -1
    best_overall_val = -float('inf')
    
    for name, (func, budget) in strategies.items():
        idx = func(budget)
        results[name] = idx
        val = get_score(idx)
        if val > best_overall_val:
            best_overall_val = val
            best_overall_idx = idx
            
    winner = max(results, key=lambda n: get_score(results[n]))
    
    return {
        "winner": winner,
        "row": results[winner],
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
    true_goals = [[row[i] for i in goal_indices] for row in rows]
    for row in rows:
        for i in goal_indices:
            row[i] = "?"

    labeled = set()
    def label(i):
        if len(labeled) >= 50 and i not in labeled:
            raise ValueError("Budget exceeded")
        labeled.add(i)
        return true_goals[i]

    result = race(header, rows, label)
    print(f"Strategy Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best Row Found: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
