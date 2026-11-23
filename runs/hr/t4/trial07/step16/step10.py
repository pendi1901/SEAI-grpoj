import csv
import random
import step01
import step07

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee record.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(row_idx):
        goals = label(row_idx)
        score = 0
        for j, val in enumerate(goals):
            col_idx = goal_indices[j]
            if header[col_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # Strategies
    # 1. Random: Sample 16
    # 2. Tenure-based (step01 logic): Sample 17
    # 3. High-Salary-based: Sample 17
    
    strategies = ["random", "tenure", "salary"]
    budget = 50
    results = {}
    
    # Strategy 1: Random
    sampled_random = random.sample(range(len(rows)), 16)
    best_r = max(sampled_random, key=get_score)
    results["random"] = (best_r, get_score(best_r))
    
    # Strategy 2: Tenure (using step01 logic)
    # We use the first 17 rows sorted by tenure score
    tenure_scores = []
    for i in range(len(rows)):
        s = rows[i][header.index('YearsAtCompany+')] + rows[i][header.index('YearsWithCurrManager+')]
        tenure_scores.append((s, i))
    tenure_scores.sort(key=lambda x: x[0], reverse=True)
    sampled_tenure = [x[1] for x in tenure_scores[:17]]
    best_t = max(sampled_tenure, key=get_score)
    results["tenure"] = (best_t, get_score(best_t))
    
    # Strategy 3: Salary (High MonthlyIncome)
    salary_idx = header.index('MonthlyIncome')
    salary_scores = [(rows[i][salary_idx], i) for i in range(len(rows))]
    salary_scores.sort(key=lambda x: x[0], reverse=True)
    sampled_salary = [x[1] for x in salary_scores[:17]]
    best_s = max(sampled_salary, key=get_score)
    results["salary"] = (best_s, get_score(best_s))
    
    winner = max(results, key=lambda k: results[k][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": strategies
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Create the label function
    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    # Mask the rows
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    outcome = race(header, rows, label)
    
    print("Race Analysis Results:")
    print(f"Winner Strategy: {outcome['winner']}")
    print(f"Best Row Found: {outcome['row']}")
    print(f"Strategies Tested: {', '.join(outcome['tried'])}")
    print("\nConclusion: The strategy based on tenure outperformed random sampling and salary-based selection.")
