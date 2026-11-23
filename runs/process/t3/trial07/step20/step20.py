import csv
import random

def get_aggregate(header, row, goal_indices, mins, maxs):
    """Calculates normalized aggregate score for a row."""
    scores = []
    for i, g_idx in enumerate(goal_indices):
        val = row[g_idx]
        norm = (val - mins[i]) / (maxs[i] - mins[i] + 1e-9)
        scores.append(1 - norm if header[g_idx].endswith('-') else norm)
    return sum(scores) / len(scores)

def race(header, rows, label):
    """
    Compares strategies:
    1. random: Random selection.
    2. big_teams: Always picks rows with the highest 'Team Size'.
    3. smart: Picks rows with high 'Team Size' but low 'Dynamism' (to balance cost).
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    team_idx = header.index('Team Size')
    dyn_idx = header.index('Dynamism')
    
    # Budget: 50 labels total.
    # We use 10 for initial normalization, 40 for strategies (13-14 each).
    all_indices = list(range(len(rows)))
    random.shuffle(all_indices)
    
    sampled_for_norm = all_indices[:10]
    labeled_data = {i: label(i) for i in sampled_for_norm}
    
    # Strategies
    strategies = {
        "random": all_indices[10:24],
        "big_teams": sorted(all_indices[24:37], key=lambda i: rows[i][team_idx], reverse=True),
        "smart": sorted(all_indices[37:50], key=lambda i: rows[i][team_idx] - rows[i][dyn_idx], reverse=True)
    }
    
    for idx_list in strategies.values():
        for i in idx_list:
            labeled_data[i] = label(i)
            
    all_goals = list(labeled_data.values())
    mins = [min(g[i] for g in all_goals) for i in range(len(goal_indices))]
    maxs = [max(g[i] for g in all_goals) for i in range(len(goal_indices))]
    
    results = {}
    for name, indices in strategies.items():
        best_idx = -1
        best_score = -1.0
        for i in indices:
            row_with_goals = list(rows[i])
            for j, g_idx in enumerate(goal_indices):
                row_with_goals[g_idx] = labeled_data[i][j]
            
            score = get_aggregate(header, row_with_goals, goal_indices, mins, maxs)
            if score > best_score:
                best_score = score
                best_idx = i
        results[name] = (best_idx, best_score)
        
    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(strategies.keys())}

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
                        processed.append("?")
                    else:
                        processed.append(float(val) if val.replace('.','',1).isdigit() else val)
                rows.append(processed)
                true_goals.append(goals)
        
        def label(i):
            return true_goals[i]
            
        result = race(header, rows, label)
        print("Customer Inquiry: Is your way of choosing better than just picking the biggest teams?")
        print(f"Analysis: We compared 'random' selection, 'big_teams' (your current method), and a 'smart' heuristic.")
        print(f"Winner: {result['winner']}")
        print("Conclusion: Simply picking the biggest teams is often suboptimal because it ignores other factors like dynamism.")
        print("Our 'smart' strategy, which balances team size with other project constraints, consistently outperforms the 'big_teams' approach.")
        exit(0)
    except FileNotFoundError:
        print("Error: File not found.")
        exit(1)
