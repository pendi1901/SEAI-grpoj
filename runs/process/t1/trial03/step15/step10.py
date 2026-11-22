import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: 'random', 'greedy', and 'hill_climber'.
    Total budget of 50 labels shared across all strategies.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    def get_score(goals):
        score = 0
        for i, val in enumerate(goals):
            name = header[goal_indices[i]]
            score += val if name.endswith('-') else -val
        return score

    memo = {}
    def get_label(i):
        if i not in memo:
            if len(memo) >= 50:
                raise Exception("Budget exceeded")
            memo[i] = label(i)
        return memo[i]

    # Strategy 1: Random sampling
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx, best_score = -1, float('inf')
        for idx in indices:
            score = get_score(get_label(idx))
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Greedy (Sample 10, then 7 nearest neighbors to best)
    def strategy_greedy():
        indices = random.sample(range(len(rows)), 10)
        best_idx, best_score = -1, float('inf')
        for idx in indices:
            score = get_score(get_label(idx))
            if score < best_score:
                best_score, best_idx = score, idx
        
        def dist(i, j):
            return sum((rows[i][k] - rows[j][k])**2 for k in input_indices)**0.5
        
        others = sorted([i for i in range(len(rows)) if i not in memo], key=lambda i: dist(i, best_idx))
        for idx in others[:7]:
            score = get_score(get_label(idx))
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Hill Climber (Start random, look at 16 neighbors)
    def strategy_hill_climber():
        curr = random.randint(0, len(rows) - 1)
        best_idx, best_score = curr, get_score(get_label(curr))
        for _ in range(16):
            n = random.randint(0, len(rows) - 1)
            score = get_score(get_label(n))
            if score < best_score:
                best_score, best_idx = score, n
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "hill_climber": strategy_hill_climber()
    }
    
    winner = min(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_data = [[float(x) for x in row] for row in reader]
        
        def label(i):
            return [full_data[i][idx] for idx in range(len(header)) if header[idx].endswith(('-', '+'))]
        
        masked_rows = []
        for row in full_data:
            masked_rows.append([row[i] if not header[i].endswith(('-', '+')) else "?" for i in range(len(row))])
            
        result = race(header, masked_rows, label)
        print(f"Race complete. Winner: {result['winner']} (found at index {result['row']}).")
        print(f"Strategies compared: {', '.join(result['tried'])}.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
