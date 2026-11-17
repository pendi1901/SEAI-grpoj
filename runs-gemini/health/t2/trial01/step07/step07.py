import csv
import step01
import step02

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them to get their true
    goal values, and returning the index of the one with the highest score.
    """
    # We have 8000 rows, we can label 50. 
    # We pick 50 indices spread across the dataset to get a representative sample.
    step = len(rows) // 50
    indices_to_test = [i * step for i in range(50)]
    
    best_idx = -1
    best_score = -float('inf')
    
    # We need to normalize based on the known data. 
    # Since we only have 50 labels, we use the provided rows (with goals as "?")
    # and the labeled goals to calculate scores.
    
    for idx in indices_to_test:
        # Get true goals for this row
        true_goals = label(idx)
        
        # Temporarily update the row with true goals to calculate score
        original_row = list(rows[idx])
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        for i, g_idx in enumerate(goal_indices):
            rows[idx][g_idx] = true_goals[i]
            
        # Calculate score using step01 logic
        # We use a subset of rows to calculate min/max for normalization
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = rows[idx][g_idx]
            # Simple normalization: use the range of the 50 sampled rows
            sampled_vals = [rows[j][g_idx] for j in indices_to_test if isinstance(rows[j][g_idx], (int, float))]
            mn, mx = min(sampled_vals), max(sampled_vals)
            rng = mx - mn
            norm = (val - mn) / rng if rng > 0 else 0
            score += (1 - norm) if header[g_idx].endswith('-') else norm
            
        if score > best_score:
            best_score = score
            best_idx = idx
            
        # Restore row
        rows[idx] = original_row
        
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if val.replace('.', '', 1).isdigit() or (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) else val for val in row]
            data.append(processed_row)

    # Define the label function as required
    def label(i):
        # Return the true goal values for the row at index i
        return [data[i][j] for j, name in enumerate(header) if name.endswith(('-', '+'))]

    # Mask goals for the choose function
    for row in data:
        for i in range(len(header)):
            if header[i].endswith(('-', '+')):
                row[i] = "?"

    best_index = choose(header, data, label)
    print(f"Analysis complete. The best setup found among the 50 sampled is at index {best_index}.")
