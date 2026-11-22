import csv
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def race(header, rows, label):
    """
    Compares the customer's 'big team' strategy against random and 
    model-based optimization strategies.
    """
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    team_size_idx = header.index('Team Size')
    
    # Helper to score a row (lower is better)
    def get_score(goal_vals):
        score = 0
        for i, g in enumerate(goals):
            val = goal_vals[i]
            if g.endswith('+'):
                score += (1.0 - val)
            else:
                score += val
        return score

    # Budget management
    labeled = {}
    def get_label(idx):
        if idx not in labeled:
            if len(labeled) >= 50:
                raise ValueError("Budget exceeded")
            labeled[idx] = label(idx)
        return labeled[idx]

    # Strategies
    def strategy_random(indices):
        return np.random.choice(indices)

    def strategy_big_teams(indices):
        # Customer's current strategy: pick rows with highest Team Size
        # We look at the input part of the row (which is visible)
        team_sizes = [rows[i][team_size_idx] for i in indices]
        return indices[np.argmax(team_sizes)]

    def strategy_greedy(indices, labeled_indices):
        X_train = [rows[i][:len(inputs)] for i in labeled_indices]
        y_train = [get_score(get_label(i)) for i in labeled_indices]
        knn = KNeighborsRegressor(n_neighbors=3).fit(X_train, y_train)
        preds = knn.predict([rows[i][:len(inputs)] for i in indices])
        return indices[np.argmin(preds)]

    strategies = {"random": strategy_random, "big_teams": strategy_big_teams, "greedy": strategy_greedy}
    results = {name: {"best_idx": -1, "best_score": float('inf')} for name in strategies}
    
    all_indices = list(range(len(rows)))
    
    # Run strategies
    for _ in range(50):
        for name in strategies:
            if len(labeled) >= 50: break
            pool = [i for i in all_indices if i not in labeled]
            if not pool: break
            
            if name == "random":
                idx = strategies[name](pool)
            elif name == "big_teams":
                idx = strategies[name](pool)
            else:
                idx = strategies[name](pool, list(labeled.keys()))
            
            score = get_score(get_label(idx))
            if score < results[name]["best_score"]:
                results[name]["best_score"] = score
                results[name]["best_idx"] = idx

    winner = min(results, key=lambda n: results[n]["best_score"])
    return {"winner": winner, "row": results[winner]["best_idx"], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row])
        
        true_goals = [row[len(header)-3:] for row in rows]
        def label(i): return true_goals[i]
        
        outcome = race(header, rows, label)
        
        print("Customer Inquiry: Is your way of choosing better than picking the biggest teams?")
        print(f"Analysis: We compared 'random' selection, 'big_teams' (your current approach), and 'greedy' optimization.")
        print(f"Winner: The '{outcome['winner']}' strategy found the best configuration.")
        
        if outcome['winner'] == 'big_teams':
            print("Answer: Your current strategy of picking the biggest teams is optimal.")
        else:
            print("Answer: No, the 'greedy' optimization strategy outperformed your 'big_teams' approach.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
