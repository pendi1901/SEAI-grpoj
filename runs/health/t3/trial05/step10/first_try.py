import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (based on first 10 samples), 
    and hill-climbing (based on first 10 samples).
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    labeled = {}
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    def get_score(row_idx):
        goals = get_label(row_idx)
        score = 0
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            # Simple normalization: assume range [0, 1] based on problem context
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # 1. Random Strategy
    def strategy_random():
        best_idx = -1
        best_score = -float('inf')
        for _ in range(16): # 16 samples
            idx = random.randint(0, len(rows) - 1)
            score = get_score(idx)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # 2. Greedy Strategy (Sample 10, pick best, then sample 6 more near it)
    def strategy_greedy():
        samples = random.sample(range(len(rows)), 10)
        best_idx = max(samples, key=get_score)
        for _ in range(6):
            idx = random.randint(0, len(rows) - 1)
            if get_score(idx) > get_score(best_idx):
                best_idx = idx
        return best_idx, get_score(best_idx)

    # 3. Hill Climbing Strategy
    def strategy_hill():
        curr = random.randint(0, len(rows) - 1)
        for _ in range(15): # 16 total labels
            neighbors = random.sample(range(len(rows)), 3)
            best_n = max(neighbors, key=get_score)
            if get_score(best_n) > get_score(curr):
                curr = best_n
        return curr, get_score(curr)

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "hill": strategy_hill()
    }

    winner = max(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "greedy", "hill"]
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)

        def label(i):
            return [rows[i][j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]

        result = race(header, rows, label)
        print(f"The winner is: {result['winner']} (found best row at index {result['row']})")
        print(f"Strategies compared: {', '.join(result['tried'])}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
