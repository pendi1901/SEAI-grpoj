import csv
import random as r
import step01

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and remember.
    Each strategy is allocated a portion of the 50-label budget.
    """
    budget = 50
    tried_indices = {}

    def get_score(row_with_goals):
        total = 0
        for i, name in enumerate(header):
            if name.endswith('-'):
                total += row_with_goals[i]
            elif name.endswith('+'):
                total += (1.0 - row_with_goals[i])
        return total

    def get_full_row(idx):
        if idx not in tried_indices:
            if len(tried_indices) >= budget:
                raise Exception("Budget exceeded")
            goals = label(idx)
            full_row = list(rows[idx])
            goal_idx = 0
            for i, name in enumerate(header):
                if name.endswith('-') or name.endswith('+'):
                    full_row[i] = goals[goal_idx]
                    goal_idx += 1
            tried_indices[idx] = full_row
        return tried_indices[idx]

    # Strategy 1: Random (16 trials)
    random_samples = r.sample(range(len(rows)), 16)
    best_random_idx = -1
    best_random_score = float('inf')
    for idx in random_samples:
        row = get_full_row(idx)
        score = get_score(row)
        if score < best_random_score:
            best_random_score = score
            best_random_idx = idx

    # Strategy 2: Greedy (17 trials)
    greedy_samples = r.sample(range(len(rows)), 17)
    best_greedy_idx = -1
    best_greedy_score = float('inf')
    for idx in greedy_samples:
        row = get_full_row(idx)
        score = get_score(row)
        if score < best_greedy_score:
            best_greedy_score = score
            best_greedy_idx = idx

    # Strategy 3: Remember (17 trials)
    rem_samples = r.sample(range(len(rows)), 17)
    rem_rows = [get_full_row(i) for i in rem_samples]
    best_rem_local_indices = step01.remember(header, rem_rows)
    best_rem_idx = rem_samples[best_rem_local_indices[0]]
    best_rem_score = get_score(rem_rows[best_rem_local_indices[0]])

    results = {
        "random": (best_random_score, best_random_idx),
        "greedy": (best_greedy_score, best_greedy_idx),
        "remember": (best_rem_score, best_rem_idx)
    }

    winner = min(results, key=lambda k: results[k][0])
    
    return {
        "winner": winner,
        "row": results[winner][1],
        "tried": ["random", "greedy", "remember"]
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        def label(i):
            return [rows[i][j] for j, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
        
        result = race(header, rows, label)
        print(f"Customer Inquiry: Three consultants, 50 trials. Who wins?")
        print(f"Answer: The winner is '{result['winner']}' strategy, finding a great setup at index {result['row']}.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
