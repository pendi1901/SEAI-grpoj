import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (nearest neighbor), and 
    a simple hill-climber. They share a 50-label budget.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    def get_score(row, goals):
        s = 0
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            if header[g_idx].endswith('-'):
                s += val
            else:
                s += (1.0 - val)
        return s

    def get_dist(r1, r2):
        d2 = 0
        for i in input_indices:
            d2 += (r1[i] - r2[i]) ** 2
        return d2 ** 0.5

    # Shared budget management
    labeled = {}
    def get_goals(i):
        if i not in labeled:
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        best_idx = -1
        best_score = float('inf')
        for _ in range(16): # 16 labels
            i = random.randint(0, len(rows) - 1)
            score = get_score(rows[i], get_goals(i))
            if score < best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    # Strategy 2: Greedy (Nearest Neighbor)
    def strategy_greedy():
        # Sample 8, then pick 8 nearest
        samples = random.sample(range(len(rows)), 8)
        best_idx = min(samples, key=lambda i: get_score(rows[i], get_goals(i)))
        best_score = get_score(rows[best_idx], get_goals(best_idx))
        
        # Find 8 nearest to best
        dists = []
        for i in range(len(rows)):
            if i not in samples:
                dists.append((get_dist(rows[best_idx], rows[i]), i))
        dists.sort()
        for _, i in dists[:8]:
            score = get_score(rows[i], get_goals(i))
            if score < best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    # Strategy 3: Hill Climber
    def strategy_hill():
        # Start at random, move to nearest neighbor if better
        curr = random.randint(0, len(rows) - 1)
        best_score = get_score(rows[curr], get_goals(curr))
        for _ in range(17): # 18 labels total
            # Find nearest
            dists = sorted([(get_dist(rows[curr], rows[i]), i) for i in range(len(rows)) if i != curr])
            found_better = False
            for _, i in dists[:5]:
                score = get_score(rows[i], get_goals(i))
                if score < best_score:
                    best_score, curr = score, i
                    found_better = True
                    break
            if not found_better: break
        return curr, best_score

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "hill": strategy_hill()
    }
    
    winner = min(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_rows = [[float(x) for x in row] for row in reader]
        
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        rows_hidden = [[("?" if i in goal_indices else val) for i, val in enumerate(r)] for r in full_rows]
        
        label_count = 0
        def label(i):
            global label_count
            label_count += 1
            return [full_rows[i][idx] for idx in goal_indices]
            
        res = race(header, rows_hidden, label)
        print(f"Winner: {res['winner']}")
        print(f"Best row found at index: {res['row']}")
        print(f"Strategies compared: {', '.join(res['tried'])}")
        print(f"Total labels used: {label_count}")
    except Exception as e:
        print(f"Error: {e}")
