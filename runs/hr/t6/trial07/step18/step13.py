import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they differ significantly.
    """
    return ezr.same(xs, ys)

def get_tenure_by_training(header, rows):
    """
    Splits 'YearsWithCurrManager+' based on whether training was high or low.
    We define 'high' as above the median training days.
    """
    train_idx = header.index('TrainingTimesLastYear')
    tenure_idx = header.index('YearsWithCurrManager+')
    
    training_days = [row[train_idx] for row in rows]
    median_training = sorted(training_days)[len(training_days) // 2]
    
    high_training = []
    low_training = []
    
    for row in rows:
        tenure = row[tenure_idx]
        if row[train_idx] >= median_training:
            high_training.append(tenure)
        else:
            low_training.append(tenure)
            
    return high_training, low_training

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    high_train, low_train = get_tenure_by_training(header, rows)
    
    # Use the certify function to check for statistical significance
    is_same = certify(high_train, low_train)
    
    print("Analysis: Do people with more training really stay longer with their manager?")
    if is_same:
        print("Result: The difference is statistically insignificant (noise).")
        print("More training does not appear to correlate with longer tenure with a manager.")
    else:
        print("Result: The difference is statistically significant (real).")
        avg_high = sum(high_train) / len(high_train)
        avg_low = sum(low_train) / len(low_train)
        print(f"Average tenure (High Training): {avg_high:.2f} years")
        print(f"Average tenure (Low Training):  {avg_low:.2f} years")
