import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify column indices
    # 'TrainingTimesLastYear' is numeric (index 29)
    # 'YearsWithCurrManager+' is numeric (index 34)
    train_idx = 29
    manager_idx = 34
    
    # Split data into two groups based on median training days
    # Median of TrainingTimesLastYear is 3.0
    median_train = 3.0
    
    low_training = [r[manager_idx] for r in rows if r[train_idx] <= median_train]
    high_training = [r[manager_idx] for r in rows if r[train_idx] > median_train]
    
    # Check if the difference is significant
    is_noise = certify(low_training, high_training)
    
    print("Analysis: Do more training days lead to longer tenure with a manager?")
    print(f"Average years with manager (Low Training <= {median_train}): {sum(low_training)/len(low_training):.2f}")
    print(f"Average years with manager (High Training > {median_train}): {sum(high_training)/len(high_training):.2f}")
    
    if is_noise:
        print("Conclusion: The observed difference is statistically insignificant (noise).")
        print("Training frequency does not appear to be a primary driver of manager tenure.")
    else:
        print("Conclusion: There is a statistically significant difference in tenure.")
        print("Training frequency appears to be a real factor in how long staff stay with their manager.")
    
    exit(0)
