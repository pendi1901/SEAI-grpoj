import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (same apart from noise), False if they significantly differ.
    """
    # Ensure lists are sorted for the statistical tests
    xs, ys = sorted(xs), sorted(ys)
    # Use ezr's statistical tests: cliffs delta and Kolmogorov-Smirnov
    # If both return True, the distributions are effectively the same.
    return ezr.cliffs(xs, ys) and ezr.ks(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Identify columns
    # 'TrainingTimesLastYear' is at index 29
    # 'YearsWithCurrManager+' is at index 34
    training_idx = 29
    manager_idx = 34

    # Split data into two groups: low training (0-2) vs high training (3-6)
    low_training = []
    high_training = []

    for row in rows:
        train_val = row[training_idx]
        mgr_val = row[manager_idx]
        
        if isinstance(train_val, (int, float)) and isinstance(mgr_val, (int, float)):
            if train_val <= 2:
                low_training.append(mgr_val)
            else:
                high_training.append(mgr_val)

    # Perform the certification
    is_noise = certify(low_training, high_training)

    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average years with manager (Low Training <= 2): {sum(low_training)/len(low_training):.2f}")
    print(f"Average years with manager (High Training > 2): {sum(high_training)/len(high_training):.2f}")
    
    if not is_noise:
        print("Result: The difference is statistically significant. The effect is real.")
    else:
        print("Result: The difference is not statistically significant. It is likely just noise.")

    exit(0)
