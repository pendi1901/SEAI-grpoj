import csv
import random
import step01
import step02
import step06

def choose(header, rows, label):
    """
    Find the best row among 50 trials.
    We use a simple strategy:
    1. Randomly sample 20 rows to get a baseline.
    2. Use the KNN-based prediction (from step02/step06) to estimate 
       the utility of the remaining rows.
    3. Label the top 30 candidates based on predicted utility.
    """
    n_rows = len(rows)
    indices = list(range(n_rows))
    
    # 1. Initial random sample
    sampled = random.sample(indices, 20)
    for i in sampled:
        label(i)
    
    # 2. Predict utility for all rows
    # We use the logic from step06 to estimate goals for all rows
    # and calculate utility
    utilities = []
    for i in range(n_rows):
        # Create a copy and mask goals
        test_row = rows[i][:]
        test_row[0], test_row[1], test_row[2] = "?", "?", "?"
        
        # Get predictions
        mre, acc, pred = step06.justify(header, rows, test_row)[0] # Simplified
        # Re-calculating utility based on predictions
        u = (1.0 - mre) + acc + pred
        utilities.append((u, i))
    
    # 3. Label top 30 remaining candidates
    utilities.sort(key=lambda x: x[0], reverse=True)
    
    labeled_count = 20
    for _, idx in utilities:
        if labeled_count >= 50:
            break
        if idx not in sampled:
            label(idx)
            labeled_count += 1
            
    # 4. Return the best row found among all labeled rows
    best_idx = -1
    best_utility = -float('inf')
    
    # We need to check the true values of all labeled rows
    for i in range(n_rows):
        # Check if row was labeled (has no '?')
        if rows[i][0] != "?":
            u = (1.0 - rows[i][0]) + rows[i][1] + rows[i][2]
            if u > best_utility:
                best_utility = u
                best_idx = i
                
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        # Keep a copy of true values to simulate the label function
        true_rows = []
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed.append(float(val))
                else:
                    processed.append(val)
            true_rows.append(processed)
            
            # Masked rows for the function
            masked = processed[:]
            masked[0], masked[1], masked[2] = "?", "?", "?"
            rows.append(masked)

    def label(i):
        rows[i] = true_rows[i]
        return true_rows[i]

    best_idx = choose(header, rows, label)
    print(f"Best setup found at index {best_idx}.")
    print(f"Goals: MRE={rows[best_idx][0]:.4f}, ACC={rows[best_idx][1]:.4f}, PRED={rows[best_idx][2]:.4f}")
