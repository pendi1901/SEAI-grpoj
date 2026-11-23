import csv

def certify(xs, ys):
    """
    Performs a simple two-sample t-test (Welch's) to determine if 
    two populations are statistically different.
    Returns True if they are likely the same (cannot reject null hypothesis),
    False if they are significantly different.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    m1, m2 = sum(xs) / n1, sum(ys) / n2
    v1 = sum((x - m1) ** 2 for x in xs) / (n1 - 1)
    v2 = sum((y - m2) ** 2 for y in ys) / (n2 - 1)
    
    # Standard error
    se = ((v1 / n1) + (v2 / n2)) ** 0.5
    if se == 0:
        return m1 == m2
    
    t_stat = abs(m1 - m2) / se
    # For a 95% confidence level, critical t-value is approx 1.96
    return t_stat < 1.96

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Goal: YearsWithCurrManager+ (index 34)
    # Condition: TrainingTimesLastYear (index 29)
    idx_goal = 34
    idx_train = 29
    
    # Split into two groups based on median training days
    all_training = [r[idx_train] for r in rows]
    median_training = sum(all_training) / len(all_training)
    
    more_training = [r[idx_goal] for r in rows if r[idx_train] > median_training]
    less_training = [r[idx_goal] for r in rows if r[idx_train] <= median_training]
    
    is_same = certify(more_training, less_training)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average tenure (More training): {sum(more_training)/len(more_training):.2f} years")
    print(f"Average tenure (Less training): {sum(less_training)/len(less_training):.2f} years")
    
    if not is_same:
        print("Result: The difference is statistically significant. Training frequency is a factor.")
    else:
        print("Result: The difference is likely just noise; no significant impact found.")
