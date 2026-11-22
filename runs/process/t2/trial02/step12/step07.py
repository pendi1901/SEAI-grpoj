import csv
from step01 import remember

def choose(header, rows, label):
    """
    Selects the best row by sampling 50 rows, labeling them, 
    and returning the index of the one with the best performance.
    """
    # Identify goal indices
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def get_score(row_goals):
        # row_goals is a list of values corresponding to goal_indices
        s = 0
        for i, (idx, op) in enumerate(goal_indices):
            val = float(row_goals[i])
            s += val if op == '-' else -val
        return s

    # We have 50 labels. We sample 50 rows evenly across the dataset.
    # If the dataset is smaller than 50, we label all of them.
    n = len(rows)
    indices_to_label = []
    if n <= 50:
        indices_to_label = list(range(n))
    else:
        step = n // 50
        indices_to_label = [i * step for i in range(50)]

    best_idx = -1
    best_score = float('inf')

    for i in indices_to_label:
        # label(i) returns the true goal values for rows[i]
        true_goals = label(i)
        score = get_score(true_goals)
        
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Mock label function for the test harness
        def label(i):
            return [rows[i][idx] for idx, _ in 
                    [(j, name[-1]) for j, name in enumerate(header) 
                     if name.endswith('-') or name.endswith('+')]]

        best_row_idx = choose(header, rows, label)
        
        print(f"The best setup found is at row index: {best_row_idx}")
        print("This row was selected after evaluating 50 samples.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
