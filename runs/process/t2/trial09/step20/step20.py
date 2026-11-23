import csv
import random

def race(header, rows, label):
    """
    Compares the customer's current strategy (biggest teams) against 
    a random search and a greedy search.
    """
    budget = 50
    tried = ["random", "greedy", "biggest_teams"]
    
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    team_size_idx = header.index('Team Size')

    def score_goals(goals):
        total = 0
        for i, (idx, op) in enumerate(goal_indices):
            val = goals[i]
            total += val if op == '-' else (1.0 - val)
        return total

    # Strategy 1: Random (16 samples)
    random_indices = random.sample(range(len(rows)), 16)
    best_random = min(random_indices, key=lambda i: score_goals(label(i)))
    
    # Strategy 2: Greedy (17 samples)
    greedy_indices = random.sample(range(len(rows)), 17)
    best_greedy = min(greedy_indices, key=lambda i: score_goals(label(i)))
    
    # Strategy 3: Biggest Teams (17 samples)
    # Sort by Team Size descending and pick the top 17
    sorted_by_size = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
    biggest_indices = sorted_by_size[:17]
    best_biggest = min(biggest_indices, key=lambda i: score_goals(label(i)))
    
    results = {
        "random": (best_random, score_goals(label(best_random))),
        "greedy": (best_greedy, score_goals(label(best_greedy))),
        "biggest_teams": (best_biggest, score_goals(label(best_biggest)))
    }
    
    winner = min(results, key=lambda k: results[k][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": tried
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_data = []
            for row in reader:
                numeric_row = [float(x) for x in row]
                rows.append(numeric_row)
                true_data.append([numeric_row[i] for i, name in enumerate(header) 
                                 if name.endswith(('-', '+'))])
            
            # Mask goals
            goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
            for row in rows:
                for idx in goal_indices:
                    row[idx] = "?"
            
            def label(i):
                return true_data[i]
            
            result = race(header, rows, label)
            
            print("Customer Inquiry: Is your way of choosing better than just picking the biggest teams?")
            print(f"Winner: {result['winner']}")
            print(f"Analysis: We compared random sampling, greedy search, and your 'biggest teams' strategy.")
            print(f"The best strategy found was '{result['winner']}'.")
            if result['winner'] == "biggest_teams":
                print("Answer: Your current strategy is actually optimal for this dataset.")
            else:
                print(f"Answer: No, '{result['winner']}' outperformed your 'biggest teams' strategy.")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
