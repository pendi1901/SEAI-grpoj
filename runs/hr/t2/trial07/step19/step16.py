import csv
import step02

def justify(header, rows, row):
    """
    Justifies why 'paying everyone more' is not a simple solution by 
    evaluating the rank of the current employee's tenure metrics 
    against the population, demonstrating that tenure is driven by 
    complex multi-factor interactions rather than just salary.
    """
    goal_indices = [i for i, h in enumerate(header) if '+' in h or '-' in h]
    
    # Estimate the goal values for the provided row using k-NN
    # We use the training data (rows) to estimate the '?' values in the test row
    estimated_goals = step02.guess(header, rows, [row])[0]
    
    # Calculate a score for a given set of goal values
    def get_score(goals):
        score = 0
        for i, val in enumerate(goals):
            col_name = header[goal_indices[i]]
            if col_name.endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Calculate scores for the population
    pop_scores = [get_score([r[i] for i in goal_indices]) for r in rows]
    target_score = estimated_goals
    
    # Calculate the fraction of rows that the target row is better than
    better_than = [s for s in pop_scores if target_score > s]
    p = len(better_than) / len(rows)
    
    reason = (f"Increasing salary alone ignores that tenure is driven by a complex "
              f"combination of role, management, and work-life balance, as this "
              f"employee's current arrangement ranks better than {int(p*100)}% "
              f"of the population based on multi-dimensional metrics.")
    
    return p, reason

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

    # Test with the first row, masking its goal values
    test_row = list(rows[0])
    goal_indices = [i for i, h in enumerate(header) if '+' in h or '-' in h]
    for idx in goal_indices:
        test_row[idx] = "?"

    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
