import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 16 random rows.
    2. 'big_team': Picks 16 rows with the largest 'Team Size'.
    3. 'greedy': Picks 16 random rows and chooses the best one.
    Total budget: 50 labels.
    """
    goal_indices = [i for i, col in enumerate(header) if col.endswith(('-', '+'))]
    team_idx = header.index('Team Size')

    def get_score(goals):
        score = 0
        for i, val in enumerate(goals):
            col_name = header[goal_indices[i]]
            if col_name.endswith('-'):
                score -= val
            else:
                score += val
        return score

    budget = 50
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        best_idx = -1
        best_score = -float('inf')
        for _ in range(16):
            idx = random.randint(0, len(rows) - 1)
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Big Team (The customer's current approach)
    def strategy_big_team():
        # Sort indices by team size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
        best_idx = -1
        best_score = -float('inf')
        # Check top 16 biggest teams
        for idx in sorted_indices[:16]:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Greedy (Sample 16, pick best)
    def strategy_greedy():
        indices = random.sample(range(len(rows)), 16)
        best_idx = -1
        best_score = -float('inf')
        for idx in indices:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "big_team": strategy_big_team(),
        "greedy": strategy_greedy()
    }

    winner = max(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "big_team", "greedy"]
    }

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_data = []
            for row in reader:
                full_data.append([float(x) for x in row])
            
        def label(i):
            goal_indices = [idx for idx, col in enumerate(header) if col.endswith(('-', '+'))]
            return [full_data[i][idx] for idx in goal_indices]

        rows = []
        for row in full_data:
            # Keep inputs, mask goals
            new_row = []
            for i, val in enumerate(row):
                if header[i].endswith(('-', '+')):
                    new_row.append("?")
                else:
                    new_row.append(val)
            rows.append(new_row)
        
        result = race(header, rows, label)
        
        print("Customer Inquiry: Is 'Big Teams' the best strategy?")
        print(f"The winning strategy is: {result['winner']}")
        print(f"The 'big_team' strategy (your current approach) was compared against others.")
        if result['winner'] == 'big_team':
            print("Our analysis confirms that your current approach is optimal.")
        else:
            print(f"Our analysis suggests that '{result['winner']}' outperforms your current 'big_team' approach.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
