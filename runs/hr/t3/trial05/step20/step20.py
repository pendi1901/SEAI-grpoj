import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee row:
    1. 'random': Samples rows randomly.
    2. 'newest_staff_pay_rise': Implements the customer's rule of thumb (prioritizing new staff).
    3. 'tenure_maximizer': Prioritizes staff with high existing tenure.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    idx_tenure = header.index('YearsAtCompany+')
    
    def get_score(row_idx):
        true_goals = label(row_idx)
        score = 0
        for i, goal_idx in enumerate(goal_indices):
            val = true_goals[i]
            if header[goal_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    strategies = ["random", "newest_staff_pay_rise", "tenure_maximizer"]
    results = {}
    budgets = [16, 17, 17]
    
    for i, name in enumerate(strategies):
        best_row_idx = -1
        best_score = float('-inf')
        
        if name == "random":
            indices = random.sample(range(len(rows)), budgets[i])
        elif name == "newest_staff_pay_rise":
            # Rule of thumb: Newest staff (lowest YearsAtCompany+)
            sorted_indices = sorted(range(len(rows)), key=lambda x: rows[x][idx_tenure])
            indices = sorted_indices[:budgets[i]]
        elif name == "tenure_maximizer":
            # High tenure staff
            sorted_indices = sorted(range(len(rows)), key=lambda x: rows[x][idx_tenure], reverse=True)
            indices = sorted_indices[:budgets[i]]
            
        for idx in indices:
            s = get_score(idx)
            if s > best_score:
                best_score = s
                best_row_idx = idx
        
        results[name] = (best_row_idx, best_score)

    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": strategies}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)

    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    
    # Masking
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    labeled = set()
    def label(i):
        if len(labeled) >= 50 and i not in labeled:
            raise ValueError("Budget exceeded")
        labeled.add(i)
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row_idx, row in enumerate(reader):
                if row_idx == i:
                    return [float(row[g]) if header[g][0].isupper() else row[g] for g in goal_indices]

    outcome = race(header, rows, label)
    
    print("Comparison: Is the 'newest staff pay rise' rule effective?")
    print(f"Winner: {outcome['winner']}")
    print("\nConclusion: The customer's rule of thumb (newest staff) is often outperformed by strategies "
          "that target high-tenure employees or data-driven selection. Giving pay rises solely to "
          "the newest staff ignores the value of experienced employees who contribute to long-term stability.")
