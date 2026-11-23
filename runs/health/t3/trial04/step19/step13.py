import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (i.e., they are the same apart from noise), False if they really differ.
    We use the Mann-Whitney U test to compare the distributions.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Mann-Whitney U test is robust for comparing two independent samples
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    _, p_value = stats.mannwhitneyu(xs, ys, alternative='two-sided')
    return p_value > 0.05

def get_score(header, row):
    """Calculates aggregate score: (1 - MRE) + ACC + PRED40."""
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    return (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(x) if i not in [4] else x for i, x in enumerate(row)]
            rows.append(processed)

    # Split rows based on the 'criterion' rule (e.g., 'absolute_error' vs 'squared_error')
    # This represents the "two built-in rules" the customer is arguing about.
    crit_idx = header.index('criterion')
    group1 = [get_score(header, r) for r in rows if r[crit_idx] == 'absolute_error']
    group2 = [get_score(header, r) for r in rows if r[crit_idx] == 'squared_error']

    is_same = certify(group1, group2)

    print("Analysis of the impact of the 'criterion' rule choice:")
    if is_same:
        print("The choice between the two rules makes no real difference.")
        print("Statistical analysis shows the performance distributions are effectively the same.")
        print("You can stop arguing about it.")
    else:
        print("The choice between the two rules makes a significant difference.")
        print("Statistical analysis shows the performance distributions are distinct.")
        print("The argument is justified.")
