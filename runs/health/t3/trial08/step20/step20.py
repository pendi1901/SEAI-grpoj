import csv
import random

def get_score(header, goals):
    """
    Calculates a normalized aggregate score for a row.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    Score = (1 - MRE) + ACC + PRED
    """
    # MRE- is at index 0, ACC+ at 1, PRED40+ at 2
    mre = goals[0]
    acc = goals[1]
    pred = goals[2]
    return (1.0 - mre) + acc + pred

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and local_search.
    Total budget: 50 labels.
    """
    strategies = ["random", "greedy", "local_search"]
    budget = 50
    labeled_data = {}
    
    def get_labeled_score(i):
        if i not in labeled_data:
            if len(labeled_data) >= budget:
                raise Exception("Budget exceeded")
            labeled_data[i] = label(i)
        return get_score(header, labeled_data[i])

    results = {}

    # 1. Random Strategy: Sample 16 random rows
    best_r = -1
    best_score_r = -float('inf')
    for _ in range(16):
        idx = random.randint(0, len(rows) - 1)
        score = get_labeled_score(idx)
        if score > best_score_r:
            best_score_r = score
            best_r = idx
    results["random"] = (best_score_r, best_r)

    # 2. Greedy Strategy: Sample 17 random rows, pick best
    best_g = -1
    best_score_g = -float('inf')
    for _ in range(17):
        idx = random.randint(0, len(rows) - 1)
        score = get_labeled_score(idx)
        if score > best_score_g:
            best_score_g = score
            best_g = idx
    results["greedy"] = (best_score_g, best_g)

    # 3. Local Search: Start at random, look at 16 neighbors
    curr = random.randint(0, len(rows) - 1)
    best_score_l = get_labeled_score(curr)
    best_l = curr
    for _ in range(16):
        neighbor = (curr + random.randint(-5, 5)) % len(rows)
        score = get_labeled_score(neighbor)
        if score > best_score_l:
            best_score_l = score
            best_l = neighbor
            curr = neighbor
    results["local_search"] = (best_score_l, best_l)

    winner = max(results, key=lambda k: results[k][0])
    
    return {
        "winner": winner,
        "row": results[winner][1],
        "tried": strategies
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_data = []
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith('-') or header[i].endswith('+'):
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        try: processed.append(float(val))
                        except ValueError: processed.append(val)
                rows.append(processed)
                true_data.append(goals)

        def label(i):
            return true_data[i]

        outcome = race(header, rows, label)
        print(f"The winning strategy is: {outcome['winner']}")
        print(f"Best row found at index: {outcome['row']}")
        print(f"Strategies compared: {', '.join(outcome['tried'])}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
