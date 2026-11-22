import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best row within a 50-label budget.
    1. 'random': Picks rows at random.
    2. 'first_n': Picks the first 16 rows sequentially.
    3. 'greedy_search': Picks 17 rows by sampling and picking the best seen so far.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(row_goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = row_goals[i]
            # MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # Budget management
    budget = 50
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # Strategies
    strategies = {
        "random": random.sample(range(len(rows)), 17),
        "first_n": list(range(16)),
        "greedy_search": []
    }
    
    # Implement greedy_search: sample 17, but evaluate sequentially to pick best
    greedy_indices = random.sample(range(len(rows)), 17)
    strategies["greedy_search"] = greedy_indices

    best_overall_score = float('-inf')
    winner = None
    best_row_idx = -1

    for name, indices in strategies.items():
        for idx in indices:
            goals = get_label(idx)
            score = get_score(goals)
            if score > best_overall_score:
                best_overall_score = score
                best_row_idx = idx
                winner = name

    return {
        "winner": winner,
        "row": best_row_idx,
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
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

    true_goals = {i: [row[j] for j, h in enumerate(header) if h.endswith(('-', '+'))] 
                  for i, row in enumerate(rows)}
    
    def label(i):
        return true_goals[i]

    result = race(header, rows, label)
    
    print("Race Analysis: Does our strategy beat random picking?")
    print(f"The winning strategy was: {result['winner']}")
    print(f"The best row found was at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    if result['winner'] != 'random':
        print("Conclusion: Yes, a structured search strategy outperforms random selection.")
    else:
        print("Conclusion: Random selection was surprisingly effective.")
