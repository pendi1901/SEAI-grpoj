import ezr

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (i.e., the difference is just noise), False if they significantly differ.
    """
    # Using ezr.same which performs cliffs, ks, and cohen tests.
    return ezr.same(xs, ys)

def analyze():
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Identify indices
    # 'TrainingTimesLastYear' is numeric
    # 'YearsWithCurrManager+' is numeric
    train_idx = header.index('TrainingTimesLastYear')
    years_idx = header.index('YearsWithCurrManager+')

    # Split data into two groups: low training (0-2) vs high training (3-6)
    # This provides a meaningful comparison of "more" vs "less" training
    low_training = [r[years_idx] for r in rows if r[train_idx] <= 2]
    high_training = [r[years_idx] for r in rows if r[train_idx] > 2]

    # Test if they are the same
    is_noise = certify(low_training, high_training)

    print("Analysis: Do people with more training stay longer with their manager?")
    if is_noise:
        print("Result: The difference is statistically insignificant (just noise).")
        print("Conclusion: More training does not appear to change the duration with the manager.")
    else:
        print("Result: There is a statistically significant difference between the groups.")
        print("Conclusion: Training levels are correlated with the time spent with the manager.")
    
    return is_noise

if __name__ == "__main__":
    analyze()
    exit(0)
