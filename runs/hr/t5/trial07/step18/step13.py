import ezr
import random

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (i.e., they are the same apart from noise).
    Returns False if they really differ.
    """
    # ezr.same uses cliffs delta and KS test to check for differences.
    # We pass eps=0 to skip the Cohen's d test, focusing on rank/distribution.
    return ezr.same(xs, ys, eps=0)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Identify indices
    # 'TrainingTimesLastYear' is at index 29
    # 'YearsWithCurrManager+' is at index 34
    train_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')

    # Split data into two groups based on training frequency
    # We define "more training" as above the median
    all_trainings = [r[train_idx] for r in rows]
    median_train = sum(all_trainings) / len(all_trainings)
    
    less_training = [r[manager_idx] for r in rows if r[train_idx] <= median_train]
    more_training = [r[manager_idx] for r in rows if r[train_idx] > median_train]

    # Perform the certification
    is_same = certify(less_training, more_training)

    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"  Average years with manager (Less Training): {sum(less_training)/len(less_training):.2f}")
    print(f"  Average years with manager (More Training): {sum(more_training)/len(more_training):.2f}")
    
    if is_same:
        print("Conclusion: The difference is statistically insignificant (noise).")
    else:
        print("Conclusion: There is a statistically significant difference between the groups.")
    
    exit(0)
