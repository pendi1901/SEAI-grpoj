import csv
import step02
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, labeling them,
    and using a Random Forest to predict the best row among all candidates.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    target_idx = goal_indices[0]
    
    # Select 50 random indices to label
    indices_to_label = random.sample(range(len(rows)), min(50, len(rows)))
    
    # Build training set from labeled data
    train_data = []
    for i in indices_to_label:
        row_copy = rows[i][:]
        row_copy[target_idx] = label(i)[0]
        train_data.append(row_copy)
        
    # Predict for all rows
    # We use step02.guess to train on our 50 samples and predict the rest
    predictions = step02.guess(header, train_data, rows)
    
    # Find the index with the highest predicted value (since goal ends in +)
    best_idx = 0
    max_val = -float('inf')
    for i, val in enumerate(predictions):
        if val > max_val:
            max_val = val
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    true_goals = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            true_goals.append(processed_row[goal_idx])
            processed_row[goal_idx] = "?"
            rows.append(processed_row)
            
    def label(i):
        return [true_goals[i]]
        
    best_row_idx = choose(header, rows, label)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at row index: {best_row_idx}")
    print(f"This row has been identified as having the highest potential for long-term retention.")
