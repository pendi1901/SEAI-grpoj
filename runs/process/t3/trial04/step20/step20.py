import csv
import random

def race(header, rows, label):
    """
    Compares the customer's 'Big Team' strategy against 'Random' and 'Hill Climbing'.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    team_size_idx = header.index('Team Size')

    def get_score(goals):
        scores = []
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            # Normalize: 0 is worst, 1 is best
            # Since we don't know global min/max, we assume [0,1] range from data
            if header[g_idx].endswith('-'):
                scores.append(1.0 - val)
            else:
                scores.append(val)
        return sum(scores) / len(scores)

    budget = 50
    tried_indices = set()

    def get_labeled_score(idx):
        if idx not in tried_indices:
            if len(tried_indices) >= budget:
                return -1.0
            tried_indices.add(idx)
        return get_score(label(idx))

    # Strategy 1: Random
    def strategy_random():
        best_idx, best_score = -1, -1.0
        for _ in range(16):
            idx = random.randint(0, len(rows) - 1)
            score = get_labeled_score(idx)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Big Teams (Customer's current way)
    def strategy_big_teams():
        # Pick 17 rows with the largest Team Size
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        best_idx, best_score = -1, -1.0
        for i in sorted_indices[:17]:
            score = get_labeled_score(i)
            if score > best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    # Strategy 3: Hill-Climbing
    def strategy_hill():
        curr = random.randint(0, len(rows) - 1)
        curr_score = get_labeled_score(curr)
        for _ in range(16):
            neighbor = random.randint(0, len(rows) - 1)
            n_score = get_labeled_score(neighbor)
            if n_score > curr_score:
                curr, curr_score = neighbor, n_score
        return curr, curr_score

    results = {
        "random": strategy_random(),
        "big_teams": strategy_big_teams(),
        "hill": strategy_hill()
    }

    winner = max(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "big_teams", "hill"]
    }

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith(('-', '+')):
                        goals.append(float(val))
                        processed.append('?')
                    else:
                        processed.append(float(val))
                rows.append(processed)
                true_goals.append(goals)

        def label(i):
            return true_goals[i]

        result = race(header, rows, label)
        print("Customer Inquiry Analysis: Strategy Comparison")
        print(f"The winning strategy is: {result['winner']}")
        print(f"Best row found at index: {result['row']}")
        print(f"Strategies compared: {', '.join(result['tried'])}")
        if result['winner'] != 'big_teams':
            print("\nConclusion: Your current 'Big Team' strategy is outperformed by smarter search methods.")
        else:
            print("\nConclusion: Your current 'Big Team' strategy is currently optimal.")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
