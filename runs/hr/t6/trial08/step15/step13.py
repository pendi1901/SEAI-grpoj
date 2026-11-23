import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable 
    (noise), False if they are significantly different.
    """
    # Reuse the certification logic from step03
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify column indices
    # 'TrainingTimesLastYear' is at index 29
    # 'YearsWithCurrManager+' is at index 34
    training_idx = 29
    manager_tenure_idx = 34
    
    # Split data into two groups based on training frequency
    # We define "more training" as > 2 days (the median/typical split)
    more_training = []
    less_training = []
    
    for row in rows:
        val = row[manager_tenure_idx]
        if isinstance(val, (int, float)):
            if row[training_idx] > 2:
                more_training.append(val)
            else:
                less_training.append(val)
    
    # Run certification
    is_noise = certify(more_training, less_training)
    
    print("Analysis: Does more training lead to longer tenure with a manager?")
    print("-" * 60)
    print(f"Group 'More Training' (n={len(more_training)}): Mean tenure = {sum(more_training)/len(more_training):.2f}")
    print(f"Group 'Less Training' (n={len(less_training)}): Mean tenure = {sum(less_training)/len(less_training):.2f}")
    
    if is_noise:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: The difference is statistically significant (real effect).")
    print("-" * 60)
