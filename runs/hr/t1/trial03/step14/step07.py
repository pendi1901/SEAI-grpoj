import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows.
    We use a simple exploration strategy: sample 50 random rows,
    label them to get their true goal values, and pick the best one.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_goals):
        """Calculates a normalized score [0, 1] for a row based on goal columns."""
        # Since we don't have the full dataset stats here, we use the 
        # relative values of the 50 sampled rows to rank them.
        scores = []
        for i, idx in enumerate(goal_indices):
            col_vals = [r[i] for r in sampled_data]
            min_v, max_v = min(col_vals), max(col_vals)
            rng = max_v - min_v if max_v != min_v else 1
            norm = (row_goals[i] - min_v) / rng
            if header[idx].endswith('-'):
                norm = 1 - norm
            scores.append(norm)
        return sum(scores) / len(scores)

    # Select 50 random indices
    indices = random.sample(range(len(rows)), min(50, len(rows)))
    
    # Label the rows
    sampled_data = []
    for i in indices:
        sampled_data.append(label(i))
        
    # Find the index of the best row among the samples
    best_score = -1.0
    best_idx = indices[0]
    
    for i, row_goals in enumerate(sampled_data):
        score = get_score(row_goals)
        if score > best_score:
            best_score = score
            best_idx = indices[i]
            
    return best_idx

def load_data(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Define the label function for the harness
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    # Mask the goals
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"The best working arrangement found is at row index {best_idx}.")
    print("This selection was determined by sampling 50 employees and identifying the one with the highest composite goal score.")
