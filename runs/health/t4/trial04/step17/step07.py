import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Selects the best row by sampling 50 candidates and evaluating them.
    Uses the scoring logic from step01 to identify the best setup.
    """
    # Identify indices for goals
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # We have 800 rows, we can label 50.
    # We pick 50 random indices to evaluate.
    indices_to_sample = random.sample(range(len(rows)), 50)
    
    best_score = -float('inf')
    best_idx = -1
    
    for i in indices_to_sample:
        # Get true values from the oracle
        goals = label(i)
        mre, acc, pred = goals[0], goals[1], goals[2]
        
        # Calculate score: (1 - MRE) + ACC + PRED40
        score = (1.0 - mre) + acc + pred
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    full_data = []
    
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
            full_data.append(processed_row)
            
    # Create masked rows for the choose function
    masked_rows = []
    for r in full_data:
        masked = r[:]
        masked[0] = masked[1] = masked[2] = "?"
        masked_rows.append(masked)
        
    def label(i):
        return [full_data[i][0], full_data[i][1], full_data[i][2]]
    
    best_index = choose(header, masked_rows, label)
    
    print(f"Analysis complete. After evaluating 50 setups, the best configuration is at index {best_index}.")
    print(f"Best setup details: {full_data[best_index]}")
