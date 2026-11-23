import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and sequential.
    Total budget: 50 labels.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_utility(row):
        return -row[mre_idx] + row[acc_idx] + row[pred_idx]

    # Total budget is 50. Split into 3 strategies: 16, 17, 17.
    # We must ensure we don't label the same row twice to save budget.
    labeled_indices = set()

    def get_label(i):
        if i not in labeled_indices:
            labeled_indices.add(i)
        return label(i)

    # Strategy 1: Random
    def strategy_random(n):
        indices = random.sample([i for i in range(len(rows)) if i not in labeled_indices], n)
        best_u = -float('inf')
        best_i = -1
        for i in indices:
            row = get_label(i)
            u = get_utility(row)
            if u > best_u:
                best_u, best_i = u, i
        return best_i, best_u

    # Strategy 2: Greedy (Sample and pick best)
    def strategy_greedy(n):
        indices = random.sample([i for i in range(len(rows)) if i not in labeled_indices], n)
        best_u = -float('inf')
        best_i = -1
        for i in indices:
            row = get_label(i)
            u = get_utility(row)
            if u > best_u:
                best_u, best_i = u, i
        return best_i, best_u

    # Strategy 3: Sequential (First n)
    def strategy_sequential(n):
        best_u = -float('inf')
        best_i = -1
        count = 0
        for i in range(len(rows)):
            if i not in labeled_indices:
                row = get_label(i)
                u = get_utility(row)
                if u > best_u:
                    best_u, best_i = u, i
                count += 1
                if count >= n:
                    break
        return best_i, best_u

    res_random = strategy_random(16)
    res_greedy = strategy_greedy(17)
    res_seq = strategy_sequential(17)

    results = {
        "random": res_random,
        "greedy": res_greedy,
        "sequential": res_seq
    }

    winner = max(results, key=lambda k: results[k][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "greedy", "sequential"]
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    def label(i):
        return rows[i]

    result = race(header, rows, label)
    print(f"Race Results: The winner is '{result['winner']}' strategy.")
    print(f"Best row found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
