import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (i.e., the difference is just noise), False if they really differ.
    Uses the same logic as ezr.same.
    """
    # Ensure lists are sorted for statistical tests
    xs, ys = sorted(xs), sorted(ys)
    # Using ezr's statistical suite: cliffs delta and KS test
    # If both return True, the distributions are considered the same.
    return ezr.cliffs(xs, ys) and ezr.ks(xs, ys)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Identify indices
    # 'TrainingTimesLastYear' is numeric
    # 'YearsWithCurrManager+' is numeric (goal to maximize)
    idx_training = header.index('TrainingTimesLastYear')
    idx_manager = header.index('YearsWithCurrManager+')

    # Split data into two groups based on training days
    # We define "more training" as > 3 days (median/mean split)
    low_training = []
    high_training = []

    for row in rows:
        val_tenure = row[idx_manager]
        val_train = row[idx_training]
        
        if val_tenure == "?" or val_train == "?":
            continue
            
        if val_train <= 3:
            low_training.append(val_tenure)
        else:
            high_training.append(val_tenure)

    # Perform certification
    is_noise = certify(low_training, high_training)

    print("Analysis: Do more training days lead to longer time with manager?")
    print("-" * 60)
    print(f"Group 'Low Training' (<=3 days, n={len(low_training)}): mean={sum(low_training)/len(low_training):.2f}")
    print(f"Group 'High Training' (>3 days, n={len(high_training)}): mean={sum(high_training)/len(high_training):.2f}")
    print("-" * 60)
    
    if is_noise:
        print("Result: The difference is statistically insignificant (noise).")
        print("Conclusion: More training does not significantly change tenure with manager.")
    else:
        print("Result: The difference is statistically significant (not just noise).")
        print("Conclusion: Training levels appear to have a real impact on tenure with manager.")
    print("-" * 60)
