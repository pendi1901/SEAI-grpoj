import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Selects the best row out of 50 attempts using a simple exploration strategy.
    We sample 50 rows, label them to get their true performance, and return the index
    of the one that performs best according to the Pareto-based ranking logic.
    """
    # We have a budget of 50 labels.
    # We will pick 50 random indices to evaluate.
    indices_to_label = random.sample(range(len(rows)), min(50, len(rows)))
    
    labeled_data = []
    for idx in indices_to_label:
        # Get true goals
        goals = label(idx)
        # Create a copy of the row with true goals filled in
        row = list(rows[idx])
        goal_idx = 0
        for i, name in enumerate(header):
            if name.endswith(('-', '+')):
                row[i] = goals[goal_idx]
                goal_idx += 1
        labeled_data.append((idx, row))
    
    # Use the logic from step01 to find the best among the labeled ones
    # We need to pass the full rows (with goals) to remember()
    all_labeled_rows = [item[1] for item in labeled_data]
    best_local_indices = remember(header, all_labeled_rows)
    
    # Map back to the original index
    best_idx_in_labeled = best_local_indices[0]
    return labeled_data[best_idx_in_labeled][0]

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
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    # Mock label function for the standalone execution
    def mock_label(i):
        goals = []
        for col_idx, name in enumerate(header):
            if name.endswith(('-', '+')):
                goals.append(rows[i][col_idx])
        return goals

    best_idx = choose(header, rows, mock_label)
    print(f"The best configuration found within the 50-setup budget is at index {best_idx}.")
