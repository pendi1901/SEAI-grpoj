import csv
import step02
import step05

def choose(header, rows, label):
    """
    Finds the best working arrangement by using 50 labels to train a model
    and then predicting the best row among the remaining ones.
    """
    # Identify goal column
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    goal_idx = header.index(goal_col)
    is_maximize = goal_col.endswith('+')

    # 1. Use 50 labels to get ground truth for a subset
    # We pick the first 50 rows to label
    labeled_indices = list(range(50))
    for i in labeled_indices:
        rows[i][goal_idx] = label(i)[0]

    # 2. Train a model using the 50 labeled rows
    # We use step02's guess logic, but we need to adapt it to use our 50 rows
    train_data = [rows[i] for i in labeled_indices]
    test_data = [rows[i] for i in range(50, len(rows))]
    
    # Mask goals in test data
    for row in test_data:
        row[goal_idx] = "?"

    # Get predictions for the remaining rows
    predictions = step02.guess(header, train_data, test_data)

    # 3. Find the index of the best row
    # Combine labeled rows and predictions
    all_scores = [rows[i][goal_idx] for i in labeled_indices] + predictions
    
    if is_maximize:
        best_val = max(all_scores)
        best_idx = all_scores.index(best_val)
    else:
        best_val = min(all_scores)
        best_idx = all_scores.index(best_val)

    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Mock label function for the harness
    def label(i):
        goal_idx = [j for j, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
        return [rows[i][goal_idx]]

    # Keep a copy of original rows to pass to choose
    rows_copy = [list(r) for r in rows]
    goal_idx = [j for j, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    for r in rows_copy:
        r[goal_idx] = "?"

    best_idx = choose(header, rows_copy, label)
    print(f"The best working arrangement found is at index {best_idx}.")
