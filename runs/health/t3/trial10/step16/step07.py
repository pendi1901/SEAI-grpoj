import csv
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def choose(header, rows, label):
    """
    Finds the best row by using an active learning approach:
    1. Sample 20 random rows to build an initial model.
    2. Use the model to predict performance for all unknown rows.
    3. Use the remaining 30 queries to sample rows with high predicted utility.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Helper to encode data
    encoders = {}
    for i in input_indices:
        if isinstance(rows[0][i], str):
            le = LabelEncoder()
            le.fit([r[i] for r in rows])
            encoders[i] = le

    def get_features(row):
        return [encoders[i].transform([row[i]])[0] if i in encoders else row[i] for i in input_indices]

    def get_score(goals):
        # Normalize goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # We use a simple weighted sum of normalized values
        mre, acc, pred = goals
        # Since we don't have global min/max easily, we use relative values
        # MRE is minimized, others maximized.
        return -mre + acc + pred

    queried_indices = []
    
    # 1. Initial random sample
    initial_indices = random.sample(range(len(rows)), 20)
    for i in initial_indices:
        label(i)
        queried_indices.append(i)

    # 2. Iterative improvement
    for _ in range(30):
        # Train model on currently known data
        X = [get_features(rows[i]) for i in queried_indices]
        y = [get_score(label(i)) for i in queried_indices]
        
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        
        # Predict scores for all unqueried rows
        best_idx = -1
        best_pred = -float('inf')
        
        for i in range(len(rows)):
            if i not in queried_indices:
                pred = model.predict([get_features(rows[i])])[0]
                if pred > best_pred:
                    best_pred = pred
                    best_idx = i
        
        label(best_idx)
        queried_indices.append(best_idx)

    # Return the index of the best row found
    final_scores = {i: get_score(label(i)) for i in queried_indices}
    return max(final_scores, key=final_scores.get)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
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

    # Store true goals to simulate the label function
    true_goals = {}
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    for i, row in enumerate(rows):
        true_goals[i] = [row[g] for g in goal_indices]
        # Mask the rows
        for g in goal_indices:
            row[g] = "?"

    def label(i):
        return true_goals[i]

    best_idx = choose(header, rows, label)
    print(f"The best configuration found is at index {best_idx}.")
    exit(0)
