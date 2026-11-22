import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows, labeling them, 
    and returning the index of the best performing one.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(goals):
        score = 0
        for i, val in enumerate(goals):
            # Minimize '-' (multiply by -1), Maximize '+' (multiply by 1)
            direction = -1 if header[goal_indices[i]].endswith('-') else 1
            score += val * direction
        return score

    # We have 800 rows. We can sample 50.
    # To be robust, we pick 50 random indices.
    indices = random.sample(range(len(rows)), min(50, len(rows)))
    
    best_idx = -1
    best_score = float('-inf')
    
    for i in indices:
        goals = label(i)
        score = get_score(goals)
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
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

    # Store true goals and mask them for the choose function
    true_goals = []
    for row in rows:
        true_goals.append([row[i] for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')])
        for i in range(len(row)):
            if header[i].endswith('-') or header[i].endswith('+'):
                row[i] = "?"

    called_indices = set()
    def label(i):
        if i not in called_indices:
            if len(called_indices) >= 50:
                raise ValueError("Limit of 50 labels exceeded.")
            called_indices.add(i)
        return true_goals[i]

    best_row_idx = choose(header, rows, label)
    
    print(f"Analysis complete. Evaluated {len(called_indices)} configurations.")
    print(f"The best configuration found is at index: {best_row_idx}")
    print(f"Performance metrics for this row: {true_goals[best_row_idx]}")
