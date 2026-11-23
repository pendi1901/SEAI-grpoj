import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling and labeling.
    We use a simple strategy: sample 50 rows, label them, and return the best.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_goals(goals):
        total = 0
        for i, (idx, op) in enumerate(goal_indices):
            val = float(goals[i])
            if op == '-':
                total += val
            else:
                total += (1.0 - val)
        return total

    # We have 800 rows. We can label 50.
    # We pick 50 random indices to sample the space.
    indices = random.sample(range(len(rows)), 50)
    
    best_score = float('inf')
    best_idx = -1
    
    for i in indices:
        goals = label(i)
        score = score_goals(goals)
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
        
        # Keep track of labeled rows to enforce the 50-limit rule
        labeled_cache = {}
        
        def label(i):
            if i not in labeled_cache:
                if len(labeled_cache) >= 50:
                    raise Exception("Limit of 50 labels exceeded.")
                # Extract goal values for the row
                row = rows[i]
                goals = [row[idx] for idx, name in enumerate(header) 
                         if name.endswith('-') or name.endswith('+')]
                labeled_cache[i] = goals
            return labeled_cache[i]

        best_idx = choose(header, rows, label)
        
        print("Customer Inquiry: Best setup found after 50 trials")
        print("-" * 60)
        print(f"The best setup found is at index: {best_idx}")
        print("Summary of the best setup:")
        for h, v in zip(header, rows[best_idx]):
            print(f"  {h}: {v}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
