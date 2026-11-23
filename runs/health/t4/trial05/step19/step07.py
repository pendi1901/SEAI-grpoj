import csv
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best setup among 50 trials.
    Strategy:
    1. Sample 50 rows across the dataset to get a representative view.
    2. Label these 50 rows to reveal their true goal values.
    3. Use the remember() logic to rank these 50 rows and return the best one.
    """
    # We have 800 rows, we can label 50. 
    # We pick 50 indices spread evenly across the dataset.
    n = len(rows)
    indices_to_label = [int(i * (n - 1) / 49) for i in range(50)]
    
    labeled_rows = []
    for idx in indices_to_label:
        # Get true goals
        goals = label(idx)
        # Create a copy of the row with revealed goals
        row = list(rows[idx])
        row[0], row[1], row[2] = goals[0], goals[1], goals[2]
        labeled_rows.append((row, idx))
    
    # Use remember() to find the best among these 50
    # remember() expects a list of rows, we extract the rows only
    just_rows = [item[0] for item in labeled_rows]
    best_local_indices = remember(header, just_rows)
    
    # best_local_indices[0] is the index in just_rows
    best_idx_in_labeled = best_local_indices[0]
    return labeled_rows[best_idx_in_labeled][1]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
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

    # Define the label function for the harness
    def label(i):
        # Return the true goal values for the row at index i
        return [rows[i][0], rows[i][1], rows[i][2]]

    # Mask the rows
    for r in rows:
        r[0] = r[1] = r[2] = "?"

    best_idx = choose(header, rows, label)
    print(f"The best setup found after 50 trials is at row index: {best_idx}")
    exit(0)
