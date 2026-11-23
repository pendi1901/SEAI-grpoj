import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee arrangement.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    
    def get_score(row_data):
        score = 0
        for idx in goal_indices:
            val = row_data[idx]
            if header[idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategies
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx, best_score = -1, -float('inf')
        for i in indices:
            score = get_score(label(i))
            if score > best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    def strategy_first_n(budget):
        best_idx, best_score = -1, -float('inf')
        for i in range(budget):
            score = get_score(label(i))
            if score > best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    def strategy_high_tenure(budget):
        # Heuristic: look at rows with high 'Age' as a proxy for potential tenure
        age_idx = header.index('Age')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][age_idx], reverse=True)
        best_idx, best_score = -1, -float('inf')
        for i in sorted_indices[:budget]:
            score = get_score(label(i))
            if score > best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    # Allocate budget: 16, 17, 17 = 50
    strategies = {
        "random": (strategy_random, 16),
        "first_n": (strategy_first_n, 17),
        "high_tenure": (strategy_high_tenure, 17)
    }

    results = {}
    for name, (func, budget) in strategies.items():
        results[name] = func(budget)

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
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    # Mask goals
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    labeled_count = 0
    def label(i):
        global labeled_count
        labeled_count += 1
        if labeled_count > 50:
            raise Exception("Budget exceeded")
        # Return original values
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            data = list(reader)
            row = data[i]
            return [float(row[idx]) if header[idx][0].isupper() else row[idx] for idx in goal_indices]

    result = race(header, rows, label)
    print(f"Strategy Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best Row Index Found: {result['row']}")
    print(f"Strategies Evaluated: {', '.join(result['tried'])}")
