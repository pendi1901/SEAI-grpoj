import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling and labeling.
    We use a simple strategy:
    1. Randomly sample 25 rows to establish a baseline.
    2. Use the remaining 25 queries to explore rows that are likely to be good
       based on the observed distribution of the first 25.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(goals):
        # goals = [mre, acc, pred]
        # Normalize: (1-MRE) + ACC + PRED
        return (1.0 - goals[0]) + goals[1] + goals[2]

    # Indices of rows we haven't labeled yet
    unlabeled = list(range(len(rows)))
    random.shuffle(unlabeled)
    
    best_idx = -1
    best_score = -float('inf')
    
    # Phase 1: Sample 25 rows to get a sense of the data
    for _ in range(25):
        if not unlabeled:
            break
        i = unlabeled.pop()
        goals = label(i)
        score = get_score(goals)
        if score > best_score:
            best_score = score
            best_idx = i
            
    # Phase 2: Simple greedy exploration
    # We pick 25 more random rows and keep the best overall
    for _ in range(25):
        if not unlabeled:
            break
        i = unlabeled.pop()
        goals = label(i)
        score = get_score(goals)
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed_row = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith('-') or header[i].endswith('+'):
                        goals.append(float(val))
                        processed_row.append("?")
                    else:
                        try:
                            processed_row.append(float(val))
                        except ValueError:
                            processed_row.append(val)
                rows.append(processed_row)
                true_goals.append(goals)

        queries_made = set()

        def label(i):
            if i not in queries_made:
                if len(queries_made) >= 50:
                    raise Exception("Limit exceeded")
                queries_made.add(i)
            return true_goals[i]

        best_idx = choose(header, rows, label)
        print(f"Optimization complete. Best row found at index: {best_idx}")
        print(f"Total queries used: {len(queries_made)}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
