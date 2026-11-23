import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 setups.
    We use a simple random sampling strategy to explore the space,
    labeling 50 rows and picking the one with the best aggregate score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(goals):
        # goals = [MRE-, ACC+, PRED40+]
        # Score = (1 - MRE) + ACC + PRED40
        return (1.0 - goals[0]) + goals[1] + goals[2]

    # Indices of rows we can sample
    indices = list(range(len(rows)))
    # Sample 50 indices
    sample_size = min(50, len(indices))
    sampled_indices = random.sample(indices, sample_size)

    best_idx = -1
    best_score = -float('inf')

    for i in sampled_indices:
        # Get true values from the oracle
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
                # Convert numeric columns, keep symbolic as strings
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Create a local copy of rows with goals masked as "?"
    masked_rows = []
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)

    # Define the label function for the harness
    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    best_idx = choose(header, masked_rows, label)
    
    print(f"After evaluating 50 setups, the best configuration found is at index {best_idx}.")
    print("This setup provides the optimal balance of MRE, ACC, and PRED40.")
