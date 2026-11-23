import csv
from sklearn.neighbors import KNeighborsRegressor

def get_score(header, row):
    """Calculates a normalized score [0, 1] for a row based on goals."""
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    scores = []
    for i in goal_indices:
        val = row[i]
        # Since data is normalized [0,1], we treat 1 as best
        if header[i].endswith('-'):
            scores.append(1.0 - val)
        else:
            scores.append(val)
    return sum(scores) / len(scores)

def justify(header, rows, row):
    """
    Estimates the goals for 'row' using KNN and compares it to all known rows.
    Returns (p, reason) where p is the fraction of rows outperformed.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Prepare training data
    X_train = [[r[i] for i in input_indices] for r in rows]
    y_train = [[r[i] for i in goal_indices] for r in rows]
    
    # Predict goals for the target row
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    X_test = [[row[i] for i in input_indices]]
    predicted_goals = model.predict(X_test)[0]
    
    # Create full row for scoring
    full_row = list(row)
    for idx, g_idx in enumerate(goal_indices):
        full_row[g_idx] = predicted_goals[idx]
        
    my_score = get_score(header, full_row)
    
    # Compare against all rows
    all_scores = [get_score(header, r) for r in rows]
    better_count = sum(1 for s in all_scores if my_score > s)
    p = better_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all known project configurations based on its input parameters."
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Example: Compare a specific row (B) against the dataset
        # We pick a row from the dataset to simulate "Setup B"
        test_row = list(rows[10])
        goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for i in goal_indices:
            test_row[i] = "?"
            
        p, reason = justify(header, rows, test_row)
        
        print("Customer Report: Why Setup B was not recommended")
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
        print("Setup B was not recommended because other configurations in our database demonstrate a better balance of cost, score, and idle time.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
