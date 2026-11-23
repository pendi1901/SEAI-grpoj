import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (i.e., the difference is just noise), False otherwise.
    """
    # Use the same logic as ezr.same, which checks cliffs and ks tests.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify column indices
    # 'TrainingTimesLastYear' is the input, 'YearsWithCurrManager+' is the goal
    idx_train = header.index("TrainingTimesLastYear")
    idx_mgr = header.index("YearsWithCurrManager+")
    
    # Define "more training" as above the median, "less" as median or below
    train_values = [float(r[idx_train]) for r in rows if r[idx_train] != "?"]
    median_train = sorted(train_values)[len(train_values) // 2]
    
    more_training = []
    less_training = []
    
    for row in rows:
        val_train = row[idx_train]
        val_mgr = row[idx_mgr]
        if val_train != "?" and val_mgr != "?":
            if float(val_train) > median_train:
                more_training.append(float(val_mgr))
            else:
                less_training.append(float(val_mgr))
    
    # Run the certification
    is_noise = certify(more_training, less_training)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Average years with manager (More training): {sum(more_training)/len(more_training):.2f}")
    print(f"Average years with manager (Less training): {sum(less_training)/len(less_training):.2f}")
    
    if is_noise:
        print("Result: The observed difference is statistically indistinguishable from noise.")
        print("Conclusion: Training frequency does not appear to have a significant impact on manager tenure.")
    else:
        print("Result: The difference is statistically significant.")
        print("Conclusion: Training frequency is linked to how long employees stay with their manager.")
