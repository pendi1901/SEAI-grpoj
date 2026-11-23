import csv
import random
from step02 import guess

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee row within a 50-label budget.
    Strategies:
    1. random: Picks 17 random rows.
    2. age_heuristic: Picks 17 rows with the highest 'Age'.
    3. model_based: Uses a Random Forest to predict 'YearsAtCompany+' and picks the top 16.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]
    
    budget = 50
    labeled = {}

    def get_val(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return -float('inf')
            labeled[i] = label(i)[0]
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 17)
        best_i = -1
        best_v = -float('inf')
        for i in indices:
            v = get_val(i)
            if v > best_v:
                best_v, best_i = v, i
        return best_i, best_v

    # Strategy 2: Age-based
    def strategy_age():
        age_idx = header.index('Age')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][age_idx], reverse=True)
        best_i = -1
        best_v = -float('inf')
        for i in sorted_indices[:17]:
            v = get_val(i)
            if v > best_v:
                best_v, best_i = v, i
        return best_i, best_v

    # Strategy 3: Model-based
    def strategy_model():
        train_idx = list(range(100))
        # Prepare training data: replace '?' with dummy values for training
        train_data = []
        for i in train_idx:
            row = list(rows[i])
            row[target_idx] = get_val(i)
            train_data.append(row)
        
        # Predict on remaining
        test_idx = list(range(100, 116))
        test_data = [list(rows[i]) for i in test_idx]
        for row in test_data: row[target_idx] = 0.0 # Dummy
        
        preds = guess(header, train_data, test_data)
        best_pred_idx = test_idx[preds.index(max(preds))]
        return best_pred_idx, get_val(best_pred_idx)

    results = {
        "random": strategy_random(),
        "age_heuristic": strategy_age(),
        "model_based": strategy_model()
    }

    winner = max(results, key=lambda k: results[k][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "age_heuristic", "model_based"]
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    original_rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            original_rows.append(processed_row)

    # Mask goals for the race
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    rows = [list(r) for r in original_rows]
    for row in rows:
        for idx in goal_indices: row[idx] = "?"

    def label(i):
        return [original_rows[i][idx] for idx in goal_indices]

    result = race(header, rows, label)
    print(f"Race complete. Winner: {result['winner']} (found at row {result['row']}).")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
