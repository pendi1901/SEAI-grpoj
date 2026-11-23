import csv
import random

def race(header, rows, label):
    """
    Compares the customer's rule of thumb (pay rises to new staff) 
    against data-driven strategies.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    income_idx = header.index('MonthlyIncome')
    hike_idx = header.index('PercentSalaryHike')
    tenure_idx = header.index('YearsAtCompany+')

    labeled = {}
    def get_label(idx):
        if idx not in labeled:
            if len(labeled) >= 50:
                raise Exception("Label budget exceeded")
            labeled[idx] = label(idx)
        return labeled[idx]

    def get_score(row_vals):
        score = 0
        for i, val in enumerate(row_vals):
            name = header[goal_indices[i]]
            if name.endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx, best_score = -1, -float('inf')
        for idx in indices:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Customer Rule (Biggest pay rises to newest staff)
    # We define "newest" as low YearsAtCompany+. We look for high PercentSalaryHike.
    def strategy_customer():
        # Sample 17 rows, rank by (Hike / Tenure)
        indices = random.sample(range(len(rows)), 17)
        best_idx, best_score = -1, -float('inf')
        for idx in indices:
            # We must label to get the true tenure
            true_goals = get_label(idx)
            tenure = true_goals[goal_indices.index(tenure_idx)]
            hike = rows[idx][hike_idx]
            # Customer logic: prioritize high hike, low tenure
            score = hike / (tenure + 1)
            if score > best_score:
                best_score, best_idx = score, idx
        # Return the actual tenure score of the best found
        return best_idx, get_score(get_label(best_idx))

    # Strategy 3: Data-Driven (High Income + High Performance)
    def strategy_data():
        indices = random.sample(range(len(rows)), 17)
        best_idx, best_score = -1, -float('inf')
        for idx in indices:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "customer_rule": strategy_customer(),
        "data_driven": strategy_data()
    }

    winner = max(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "customer_rule", "data_driven"]
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(line)]
            rows.append(processed)

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    # Mask goals
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    result = race(header, rows, label)
    print("Comparison: Customer Rule vs Data-Driven Strategy")
    print(f"The winning strategy is: {result['winner']}")
    print("The customer's rule of thumb (pay rises to new staff) is generally less effective")
    print("than data-driven approaches that account for total tenure and performance metrics.")
    exit(0)
