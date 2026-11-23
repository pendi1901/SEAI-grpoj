import csv
import random
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def get_utility(row):
    # MRE- (0), ACC+ (1), PRED40+ (2)
    # Ensure we are using the true values (floats)
    return (1.0 - float(row[0])) + float(row[1]) + float(row[2])

def transform(row, goal_indices):
    new_row = []
    for i, val in enumerate(row):
        if i in goal_indices: continue
        if isinstance(val, str):
            new_row.append(float(hash(val) % 1000))
        else:
            new_row.append(float(val))
    return new_row

def race(header, rows, label):
    goal_indices = [0, 1, 2]
    n_rows = len(rows)
    
    # We must track which indices have been labeled to avoid double-counting the budget
    labeled_indices = set()

    def safe_label(i):
        if i not in labeled_indices:
            label(i)
            labeled_indices.add(i)
        return rows[i]

    def strategy_random(budget):
        indices = random.sample(range(n_rows), budget)
        for i in indices: safe_label(i)
        return max(indices, key=lambda i: get_utility(rows[i]))

    def strategy_knn(budget):
        # Start with 5 random
        initial = random.sample(range(n_rows), 5)
        for i in initial: safe_label(i)
        
        for _ in range(budget - 5):
            labeled_list = list(labeled_indices)
            X_train = [transform(rows[i], goal_indices) for i in labeled_list]
            y_train = [get_utility(rows[i]) for i in labeled_list]
            model = KNeighborsRegressor(n_neighbors=min(len(labeled_list), 3)).fit(X_train, y_train)
            
            best_u, best_i = -float('inf'), -1
            for i in range(n_rows):
                if i not in labeled_indices:
                    u = model.predict([transform(rows[i], goal_indices)])[0]
                    if u > best_u: best_u, best_i = u, i
            if best_i != -1: safe_label(best_i)
        return max(list(labeled_indices), key=lambda i: get_utility(rows[i]))

    def strategy_greedy(budget):
        # Sample every Nth row
        indices = list(range(0, n_rows, n_rows // budget))[:budget]
        for i in indices: safe_label(i)
        return max(indices, key=lambda i: get_utility(rows[i]))

    # Budget 50 shared: 16, 17, 17
    best_random = strategy_random(16)
    best_knn = strategy_knn(17)
    best_greedy = strategy_greedy(17)
    
    results = {
        "random": (get_utility(rows[best_random]), best_random),
        "knn": (get_utility(rows[best_knn]), best_knn),
        "greedy": (get_utility(rows[best_greedy]), best_greedy)
    }
    
    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": ["random", "knn", "greedy"]}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    true_rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            true_rows.append([float(v) if header[i][0].isupper() else v for i, v in enumerate(row)])
    
    rows = [["?" if i < 3 else r[i] for i in range(len(r))] for r in true_rows]
    
    def label(i):
        rows[i] = true_rows[i]
        return true_rows[i]

    result = race(header, rows, label)
    print(f"Winner: {result['winner']} strategy.")
    print(f"Best row found at index {result['row']} with utility {get_utility(rows[result['row']]):.4f}.")
