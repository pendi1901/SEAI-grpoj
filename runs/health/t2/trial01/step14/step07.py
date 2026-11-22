import csv
import step01
import step02
import random

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them,
    and returning the index of the one with the highest multi-objective score.
    """
    n = len(rows)
    # We have a budget of 50 labels.
    # We pick 50 random indices to sample the space.
    indices = random.sample(range(n), min(n, 50))
    
    scored = []
    for i in indices:
        # Get true goals
        goals = label(i)
        # Update the row with the true goals
        for j in range(3):
            rows[i][j] = goals[j]
        
        # Calculate score using step01 logic
        # We need to score this row relative to the known data
        # Since we only have 50 labels, we use the 50 labeled rows as our population
        # to calculate relative rank.
        scored.append((i, goals))

    # Re-use step01 logic to score the 50 labeled rows
    # Extract goals from the labeled rows
    labeled_rows = []
    for i, goals in scored:
        row = list(rows[i])
        row[0], row[1], row[2] = goals[0], goals[1], goals[2]
        labeled_rows.append(row)
    
    # Get the best index from the labeled subset
    best_local_idx = step01.remember(header, labeled_rows)[0]
    return scored[best_local_idx][0]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed.append(float(val))
                    else:
                        processed.append(val)
                # Hide goals
                true_goals.append([processed[0], processed[1], processed[2]])
                processed[0], processed[1], processed[2] = "?", "?", "?"
                rows.append(processed)

        def label(i):
            return true_goals[i]

        best_idx = choose(header, rows, label)
        print(f"Best setup found at index: {best_idx}")
        print(f"Goals (MRE-, ACC+, PRED40+): {true_goals[best_idx]}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
