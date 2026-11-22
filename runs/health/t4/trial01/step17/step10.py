import csv
import random
from step01 import remember
from step07 import choose

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 17 random rows.
    2. 'first': Picks the first 17 rows.
    3. 'last': Picks the last 16 rows.
    """
    budget = 50
    strategies = ["random", "first", "last"]
    
    # Allocate budget: 17 + 17 + 16 = 50
    allocations = {"random": 17, "first": 17, "last": 16}
    
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(row_idx):
        goals = label(row_idx)
        mre, acc, pred = goals[idx_mre], goals[idx_acc], goals[idx_pred]
        return (1.0 - mre) + acc + pred

    results = {}
    
    # Strategy: random
    rand_indices = random.sample(range(len(rows)), allocations["random"])
    results["random"] = max([(get_score(i), i) for i in rand_indices], key=lambda x: x[0])
    
    # Strategy: first
    first_indices = list(range(allocations["first"]))
    results["first"] = max([(get_score(i), i) for i in first_indices], key=lambda x: x[0])
    
    # Strategy: last
    last_indices = list(range(len(rows) - allocations["last"], len(rows)))
    results["last"] = max([(get_score(i), i) for i in last_indices], key=lambda x: x[0])
    
    # Determine winner
    winner = max(results, key=lambda s: results[s][0])
    
    return {
        "winner": winner,
        "row": results[winner][1],
        "tried": strategies
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            rows.append(processed)

    def label(i):
        return [rows[i][0], rows[i][1], rows[i][2]]

    outcome = race(header, rows, label)
    
    print(f"Race Results:")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
    print(f"The winner is '{outcome['winner']}' which found the best configuration at index {outcome['row']}.")
