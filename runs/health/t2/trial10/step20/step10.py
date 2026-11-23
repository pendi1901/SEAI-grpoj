import csv
import random
import step01

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (best neighbor), and 
    a simple heuristic search (best of a sample).
    """
    budget = 50
    labeled = {}

    def get_goals(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    def score_row(i):
        goals = get_goals(i)
        # Use step01 normalization logic
        mre_idx = header.index('MRE-')
        acc_idx = header.index('ACC+')
        pred_idx = header.index('PRED40+')
        
        # We need global min/max for normalization. 
        # Since we only have partial labels, we use the full dataset 
        # range if available, or just the current row's values.
        # For simplicity, we use the row's values relative to the 
        # known best/worst in the dataset.
        mre, acc, pred = goals[0], goals[1], goals[2]
        # Normalize (0 to 1)
        s1 = 1 - (mre / 1.0) # MRE-
        s2 = acc / 1.0       # ACC+
        s3 = pred / 1.0      # PRED40+
        return (s1 + s2 + s3) / 3

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_i = -1
        best_s = -1
        for i in indices:
            s = score_row(i)
            if s > best_s:
                best_s, best_i = s, i
        return best_i, best_s

    # Strategy 2: Greedy (Sample 16, then pick neighbors)
    def strategy_greedy():
        indices = random.sample(range(len(rows)), 16)
        best_i = max(indices, key=score_row)
        return best_i, score_row(best_i)

    # Strategy 3: Heuristic (Sample 18)
    def strategy_heuristic():
        indices = random.sample(range(len(rows)), 18)
        best_i = max(indices, key=score_row)
        return best_i, score_row(best_i)

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "heuristic": strategy_heuristic()
    }

    winner = max(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "greedy", "heuristic"]
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        def label(i):
            row = rows[i]
            return [row[j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
        outcome = race(header, rows, label)
        print(f"Winner: {outcome['winner']}")
        print(f"Best row index found: {outcome['row']}")
        print(f"Strategies tried: {', '.join(outcome['tried'])}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
